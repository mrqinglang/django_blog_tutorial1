# --*-- coding: utf-8 --*--
# @Time     : 2020/7/25 9:19
# @Author   : mrqinglang
# @software : PyCharm
from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    # 用户退出
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    # 用户删除
    path('delete/<int:id>/', views.user_delete, name='delete'),
    # 用户信息
    path('edit/<int:id>/', views.profile_edit, name='edit'),
]