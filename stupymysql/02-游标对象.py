"""
	游标对象：
		通过连接对象的方法 cursor() 获取 ---- 作用：通过它才能操作数据库
"""
from util import MySQLUtil
# 获取连接对象
conn = MySQLUtil.get_conn()
# 获取游标对象
cur = conn.cursor()
print('游标对象：\n', cur)