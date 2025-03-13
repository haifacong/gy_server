from ultralytics import YOLO
from PIL import Image
from django.http import JsonResponse
from time import time
import re
import pymysql
from datetime import datetime
from util import MySQLUtil
import cv2
import numpy as np


# 获取数据库连接
# 获取数据库连接
def detectImg(request):
    """
    通过 request 对象获取上传的文件 api：
    file = request.FILES.get(key)
    """
    # 通过 request 对象获取上传的文件
    username = request.POST.get('username')  # 获取登录用户名
    file = request.FILES.get('file')
    filename = file.name
    reStr = re.split(r'\.(?=[^.]*$)', filename)
    timestamp = int(time())
    newFilename = reStr[0] + '_' + str(timestamp) + '.' + reStr[1]

    # 保存文件到磁盘
    with open('static/upload/' + newFilename, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)

    # 模型加载并推理
    model = YOLO(model='C:\\Users\\HaiFacong\\Desktop\\实训工地佩戴工服头盔检测项目\\gy_server\\best.pt')
    img_path = "C:\\Users\\HaiFacong\\Desktop\\实训工地佩戴工服头盔检测项目\\gy_server\\static\\upload\\" + newFilename
    results = model(img_path)

    # 获取检测结果的图像数据和检测框信息
    data = results[0].plot()  # 使用 plot() 获取渲染后的图像数据

    # 转换图像数据格式，从 BGR 转换为 RGB
    im0 = np.array(data)  # 将图像数据转换为 numpy 数组（原数据格式是 BGR）
    im0 = cv2.cvtColor(im0, cv2.COLOR_BGR2RGB)  # 转换为 RGB 格式

    # 获取检测框信息（直接通过 boxes 属性）
    boxes = results[0].boxes
    detections = []

    # 获取类别名称应该是通过 model.names 来获取，而不是通过 results[0].names
    class_names = model.names  # 这是 YOLO 模型的类别名称映射

    # 创建一个字典来记录每个类别的最高置信度
    class_scores = {}

    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()  # 获取检测框的坐标
        conf = box.conf[0].item()  # 获取置信度
        class_id = int(box.cls[0].item())  # 获取类别ID
        class_name = class_names[class_id]  # 获取类别名称

        # 更新字典，保存该类别的最高置信度
        if class_name not in class_scores or conf > class_scores[class_name]['confidence']:
            class_scores[class_name] = {
                'bbox': [x1, y1, x2, y2],
                'confidence': conf
            }

    # 将类别和最大置信度的数据存储到检测结果列表中
    for class_name, score_data in class_scores.items():
        detections.append({
            'class_name': class_name,
            'confidence': score_data['confidence'],
            'bbox': score_data['bbox']
        })

    print('最终检测结果：\n', detections)

    # 保存检测结果图像
    saveImg = Image.fromarray(im0)  # 将图像数据转换为 PIL 图像对象
    saveImg.save('C:\\Users\\HaiFacong\\Desktop\\实训工地佩戴工服头盔检测项目\\gy_server\\static\\detect\\' + newFilename)

    # 插入数据到数据库
    conn = MySQLUtil.get_conn()
    cur = conn.cursor()

    try:
        # 插入每个检测框的类别信息
        sql = """
            INSERT INTO result (detect_url, result_url, clazz, score, detect_time, username)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        detect_url = 'static/upload/' + newFilename
        result_url = 'static/detect/' + newFilename
        detect_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 遍历所有检测结果（按类别聚合）
        for detection in detections:
            clazz = detection['class_name']  # 获取每个检测框的类别名称
            score = detection['confidence']  # 获取每个检测框的置信度得分

            # 将检测结果插入数据库
            cur.execute(sql, [detect_url, result_url, clazz, score, detect_time, username])

        # 提交所有的插入操作
        conn.commit()
    except Exception as e:
        conn.rollback()
        print('数据库操作发生了异常:\n', e)
    finally:
        cur.close()
        conn.close()

    resData = {
        'status': 200,
        'msg': '检测成功',
        'data': 'http://localhost:8000/static/detect/' + newFilename
    }

    # 返回响应
    return JsonResponse(resData)