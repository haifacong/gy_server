import pymysql


# 定义一个获取数据库连接对象的方法
def get_conn():
	# 匿名对象的方式返回连接对象
	"""
		匿名对象：
			在只需要使用创建对象一次的情况下或者直接返回创建的对象的时候使用
	"""
	return pymysql.connect(
		host='localhost',  # 数据库主机地址
		port=3306,  # 数据库启动的端口号
		user='root',  # 连接数据库的账号
		password='hfc159820',  # 连接数据库账号对应的密码
		database='gy_yolo',  # 连接数据库的名称
		charset='utf8'  # 编码方式
	)
