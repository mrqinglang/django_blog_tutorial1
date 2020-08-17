# --*-- coding: utf-8 --*--
# @Time     : 2020/7/23 22:02
# @Author   : mrqinglang
# @software : PyCharm
from django import forms
from .models import ArticlePost

# 写文章的表单类
class ArticlePostForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = ArticlePost
        # 定义表单包含的字段
        fields = ('title', 'body','tags', 'avatar')