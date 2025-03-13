import json
import pymysql
from django.http import JsonResponse
from util import MySQLUtil


def fetch_users(request):
    jsonData = request.body
    userSearch = json.loads(jsonData)

    # 确保字典中存在所需的键
    username = userSearch.get('username', '')
    userCurrentPage = int(userSearch.get('userCurrentPage', 1)) - 1
    userPageSize = int(userSearch.get('userPageSize', 5))

    conn = MySQLUtil.get_conn()
    cur = conn.cursor()

    # 查询总记录数
    total_sql = 'SELECT COUNT(*) FROM user WHERE username LIKE %s'
    cur.execute(total_sql, (f"%{username}%"))
    userTotal = cur.fetchone()[0]

    # 查询用户数据
    sql = 'SELECT * FROM user WHERE username LIKE %s LIMIT %s OFFSET %s'
    cur.execute(sql, (f"%{username}%", userPageSize, userCurrentPage * userPageSize))
    result = cur.fetchall()

    resultList = []
    for item in result:
        resultList.append({'username': item[0], 'password': item[1]})

    cur.close()
    conn.close()

    return JsonResponse({'status': 200, 'data': resultList, 'total': userTotal, 'current_page': userCurrentPage + 1})


def fetch_results(request):
    jsonData = request.body
    resultSearch = json.loads(jsonData)

    # 确保字典中存在所需的键
    keyword = resultSearch.get('keyword', '')
    resultCurrentPage = int(resultSearch.get('resultCurrentPage', 1)) - 1
    resultPageSize = int(resultSearch.get('resultPageSize', 5))

    conn = MySQLUtil.get_conn()
    cur = conn.cursor()

    # 查询总记录数
    total_sql = 'SELECT COUNT(*) FROM result WHERE clazz LIKE %s'
    cur.execute(total_sql, (f"%{keyword}%"))
    resultTotal = cur.fetchone()[0]

    # 查询结果数据
    sql = 'SELECT * FROM result WHERE clazz LIKE %s LIMIT %s OFFSET %s'
    cur.execute(sql, (f"%{keyword}%", resultPageSize, resultCurrentPage * resultPageSize))
    result = cur.fetchall()

    resultList = []
    for item in result:
        resultList.append({
            'detect_url': item[0], 'result_url': item[1], 'clazz': item[2], 'score': item[3],
            'detect_time': item[4], 'username': item[5]
        })

    cur.close()
    conn.close()

    return JsonResponse(
        {'status': 200, 'data': resultList, 'total': resultTotal, 'current_page': resultCurrentPage + 1})