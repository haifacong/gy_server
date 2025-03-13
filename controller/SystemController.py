"""
	用来定义提供给前端访问的函数的文件
"""
# 导入 render 函数
from django.shortcuts import render


# 访问 index.html 页面的函数
def index(request):
	print('index 函数执行了，即将跳转到 index.html 页面！')
	"""
		render 函数参数：
			1、request 请求对象
			2、页面访问路径，以 templates 为根
			3、返回的数据内容（字典），这个数据内容在返回的页面上可以通过 {{key}} 的方式取出来
	"""
	return render(request, 'index.html', {'name': '小明', 'age': 18})


# 访问 detect.html 页面的函数
def detect(request):
	return render(request, 'detect.html')


# 访问 welcome.html 页面的函数
def welcome(request):
	return render(request, 'welcome.html')


# 访问 login.html 页面的函数
def login(request):
	return render(request, 'login.html')

def datamanage(request):
	return render(request, 'datamanage.html')

def change_password(request):
	return render(request, 'change_password.html')