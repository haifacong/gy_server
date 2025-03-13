import json

import pymysql
from django.http import JsonResponse
from util import MySQLUtil


def login(request):
    print('login 函数执行了，即将返回 json 数据！')

    # 通过 request 对象获取前端传过来的 json 数据，数据类型是 bytes
    jsonData = request.body
    # 把 bytes 转成 dict
    user = json.loads(jsonData)
    # 分别获取账号和密码
    username = user['username']
    password = user['password']

    # 获取数据库连接
    db = MySQLUtil.get_conn()
    cursor = db.cursor()

    try:
        # 查询账号是否存在
        cursor.execute("SELECT password FROM user WHERE username=%s", (username))
        result = cursor.fetchone()

        # 验证账号是否存在
        if result is None:
            return JsonResponse({'status': 404, 'msg': '账号不存在', 'data': None})
        stored_password = result[0]
        if stored_password != password:
            return JsonResponse({'status': 401, 'msg': '密码错误', 'data': None})

            # 登录成功
        return JsonResponse({'status': 200, 'msg': '登录成功', 'data': None})

    finally:
        # 关闭数据库连接
        cursor.close()
        db.close()