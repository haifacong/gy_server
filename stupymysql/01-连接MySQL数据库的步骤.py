"""
	1.导入 pymysql
	2.通过 pymysql 的方法 connect ---- 获取数据库的连接对象，这个对象一般命名为 conn
"""
import pymysql

conn = pymysql.connect(
	host='localhost',   # 数据库主机地址
	port=3306,   # 数据库启动的端口号
	user='root',   # 连接数据库的账号
	password='112112',   # 连接数据库账号对应的密码
	database='gy_yolo',   # 连接数据库的名称
	charset='utf8'   # 编码方式
)
print('连接对象：\n', conn)