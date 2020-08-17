# --*-- coding: utf-8 --*--
# @Time     : 2020/7/25 7:31
# @Author   : mrqinglang
# @software : PyCharm
# 引入表单类
from django import forms
# 引入 User 模型
from django.contrib.auth.models import User
from .models import Profile

# 登录表单，继承了 forms.Form 类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField()
    password2 = forms.CharField()
    class Meta:
        model = User
        fields = ('username', 'email')
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError('密码输出不一致，请重试。')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')