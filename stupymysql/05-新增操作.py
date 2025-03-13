"""
	向 user 表中新增一条数据
	对应增删改操作，需要手动的提交事务（做事务管理）
	try:
		把可能发生异常的代码写在这里，如果不发生异常，执行完就去 finally
		如果发生异常，就不会在执行 try 中发生异常之后的代码，直接去执行 except 中代码，执行完就去 finally
	except Exception as e:
	    当 try 中发生异常才会执行
	finally:
		无论怎样都要执行
"""
from util import MySQLUtil
conn = MySQLUtil.get_conn()
cur = conn.cursor()
try:
	username = input('请输入用户名：\n')
	password = input('请输入密码：\n')
	sql = 'insert into `user` values (%s, %s)'
	cur.execute(sql, [username, password])
	# 提交事务：没有发生任何异常
	conn.commit()
	print('成功的执行完成新增操作')
except Exception as e:
	# 回滚事务：发生异常
	conn.rollback()
	print('新增操作发生了异常：\n', e)
finally:
	cur.close()
	conn.close()