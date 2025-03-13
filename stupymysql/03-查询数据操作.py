from util import MySQLUtil
# 获取连接对象
conn = MySQLUtil.get_conn()
# 获取游标对象
cur = conn.cursor()
# 定义执行的 SQL 语句：如果怕写错，就在 Navicat 中写对了在复制过来
sql = 'select * from `user`'
# 执行 SQL 语句
"""
	cur.execute(sql, 参数列表[optional])
	这个参数列表的类型只能是：tuple, list or dict
	什么时候使用呢？
	当定义的 SQL 语句中存在 %s 占位符的时候使用
"""
cur.execute(sql)
# 获取查询的结果
"""
	cur.fetchall()：获取所有的查询结果内容，是一个元组
"""
result = cur.fetchall()
print('查询结果：\n', result)
# 关闭连接
cur.close()
conn.close()