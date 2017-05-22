# -*- coding: utf-8 -*-
# 表单

from django.http import JsonResponse
from django.shortcuts import render_to_response

from society.models import User


# 验证在线状态
def is_alive(request):
    username = request.COOKIES.get('username', '')
    if username is not None and len(User.objects.filter(username__exact=username)) > 0:
        return True
    return False


# 注册
def regist(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    email = request.POST.get('email', '')
    nickname = request.POST.get('nickname', '')
    user = User.objects.filter(username__exact=username)
    if user:
        return JsonResponse({'ok': False, 'reason': '用户名已存在'})
    else:
        User.objects.create(username=username, password=password, email=email, nickname=nickname)
        return JsonResponse({'ok': True})


# 登录
def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = User.objects.filter(username__exact=username, password__exact=password)
    if user:
        return JsonResponse({'ok': True, 'nickname': user[0].nickname})
    else:
        return JsonResponse({'ok': False})


# 退出
def logout(request):
    nickname = request.COOKIES.get('nickname', '')
    response = render_to_response('res/views/logout.html', {'nickname': nickname})
    response.delete_cookie('username')
    response.delete_cookie('nickname')
    return response
