from util import MySQLUtil
# 获取连接对象
conn = MySQLUtil.get_conn()
# 获取游标对象
cur = conn.cursor()
# python 中通过 input 函数接收键盘的输入
inputData = input('请输入要查询的 username：\n')
# 定义 SQL 语句 --- 查询username=输入的字符串的数据
# %s：占位符，通过游标对象执行 SQL 的时候，需要传递参数给这个占位符，有顺序问题
sql = 'select * from `user` where `username`=%s'
# 执行 SQL 语句
cur.execute(sql, [inputData])
# 获取查询的结果
result = cur.fetchall()
print('查询结果：\n', result)
# 关闭连接
cur.close()
conn.close()