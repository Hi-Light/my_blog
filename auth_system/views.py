import json

from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.defaultfilters import lower
from auth_system.models import MyUser


# Create your views here.
# 注册时的验证函数


def is_exist(request):
    name = request.POST['name']
    email = lower(request.POST['email'])
    if MyUser.objects.filter(name=name).__len__():
        msg_name = '用户名已存在，换一个吧'
    else:
        msg_name = ''
    if name == '':
        msg_name = '请输入用户名'
    if MyUser.objects.filter(email=email).__len__():
        msg_email = '邮箱已被使用，换一个吧'
    else:
        msg_email = ''
    if email == '':
        msg_email = ''
    return HttpResponse(json.dumps({"msg_name": msg_name, "msg_email": msg_email}))


# 登入用户
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        url = request.POST['url']
        a = MyUser.objects.filter(email=email)
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(url)
        else:
            return render(request, 'warning.html', {'information': '密码或账户不正确，请重试', 'back_url': 'ss'})


# 注销用户
def logout_user(request):
    url = request.GET['url']
    auth.logout(request)
    return HttpResponseRedirect(url)
