import json  # 导入 json 库，用于解析和生成 JSON 数据

from django.http import JsonResponse  # 导入 JsonResponse，用于返回 JSON 格式的响应
from django.views.decorators.csrf import csrf_exempt  # 导入 csrf_exempt 装饰器，允许绕过 CSRF 保护

from util import MySQLUtil  # 导入数据库引用函数



def register(request):
    # 检查请求的方法是否为 POST
    global connection
    if request.method == 'POST':
        try:  # 开始尝试执行以下代码块
            # 解析请求体中的 JSON 数据
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')  # 从数据中获取用户名
            password = data.get('password')  # 从数据中获取密码

            # 检查用户名和密码是否为空
            if not username or not password:
                # 返回错误消息，状态码为 400
                return JsonResponse({'status': 400, 'msg': '用户名和密码不能为空'})

            # 获取数据库连接
            connection = MySQLUtil.get_conn()
            # 创建游标，执行 SQL 语句
            with connection.cursor() as cursor:
                # 检查用户名是否已存在
                cursor.execute("SELECT * FROM user WHERE username=%s", (username,))
                if cursor.fetchone():  # 如果查询结果不为空
                    # 返回错误消息，状态码为 400
                    return JsonResponse({'status': 400, 'msg': '用户名已存在'})

                # 插入新用户数据到数据库
                cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, password))
                connection.commit()  # 提交事务，保存更改

            # 返回成功消息，状态码为 200
            return JsonResponse({'status': 200, 'msg': '注册成功'})
        except Exception as e:  # 捕获可能发生的异常
            # 返回错误消息，状态码为 500
            return JsonResponse({'status': 500, 'msg': str(e)})
        finally:
            # 确保数据库连接被关闭以释放资源
            connection.close()
    else:
        # 如果请求方法不是 POST，返回错误消息，状态码为 405
        return JsonResponse({'status': 405, 'msg': '方法不被允许'})