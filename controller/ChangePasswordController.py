import json  # 导入 json 库，用于解析和生成 JSON 数据

from django.http import JsonResponse  # 导入 JsonResponse，用于返回 JSON 格式的响应
from django.views.decorators.csrf import csrf_exempt  # 导入 csrf_exempt 装饰器，允许绕过 CSRF 保护

from util import MySQLUtil  # 导入数据库引用函数


@csrf_exempt
def changepassword(request):
    conn = MySQLUtil.get_conn()
    cur = conn.cursor()
    data = json.loads(request.body)

    username = data.get('username')
    newPassword = data.get('newPassword')
    print(username+':'+newPassword)#已知账号密码正确地传入进来并且值是对的,admin:123
    changeSQL = 'update user set password=%s where username=%s'
    checkSQL = 'select password from user where username=%s'
    cur.execute(checkSQL, (username))
    result = cur.fetchone()
    print(result[0])
    if result != newPassword:
        cur.execute(changeSQL,(newPassword, username))
        conn.commit()
        return JsonResponse({'status': 200, 'msg': '修改成功'})
    else:
        return JsonResponse({'status': 401, 'msg': '新老密码一致'})


def imgList(request):
    # 更新为 GET 方法，获取用户名
    username = request.GET.get('username')  # 使用 GET 方法来获取参数

    if not username:
        return JsonResponse({'status': 401, 'message': 'User not authenticated'}, status=401)

    conn = MySQLUtil.get_conn()
    cur = conn.cursor()

    sql = 'SELECT result_url FROM result WHERE username = %s'
    cur.execute(sql, (username,))
    result = cur.fetchall()

    resultList = [{'url': item[0]} for item in result]

    return JsonResponse({'status': 200, 'data': resultList})