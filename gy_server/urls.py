"""gy_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from controller import SystemController as sc
from controller import UserController as uc
from controller import DetectController as dc
from controller import DataManageController as dmc
from controller import RegisterController as RS
from controller import ChangePasswordController as cpc

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',sc.index,name='index'),
    path('detect/',sc.detect,name='detect'),
    path('welcome/',sc.welcome,name='welcome'),
    path('datamanage/',sc.datamanage,name='datamanage'),
    path('',sc.login,name='login'),
    path('login/',uc.login),
    path('detectImg/',dc.detectImg),
    path('register/', RS.register),

    path('fetch_users/', dmc.fetch_users,name='fetch_users'),
    path('fetch_results/', dmc.fetch_results,name='fetch_results'),

    path('change_password/',sc.change_password,name='change_password'),
    path('changepassword/',cpc.changepassword,name='changepassword'),
    path('imgList/',cpc.imgList,name='imgList'),
]
