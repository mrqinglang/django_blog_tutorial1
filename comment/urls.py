# --*-- coding: utf-8 --*--
# @Time     : 2020/8/4 9:37
# @Author   : mrqinglang
# @software : PyCharm
from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    # 发表评论
    path('post-comment/<int:article_id>/',views.post_comment, name='post_comment')
]