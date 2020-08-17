# --*-- coding: utf-8 --*--
# @Time     : 2020/8/4 9:25
# @Author   : mrqinglang
# @software : PyCharm
from django import forms
from .models import Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']