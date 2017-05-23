# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import IntegrityError
from django.http import JsonResponse

# 获取登录状态
from users.models import User


# Create your views here.


def status(request):
    if 'uid' in request.session:
        username = request.session.get('username', '')
        return JsonResponse({'status': True, 'username': username})
    else:
        return JsonResponse({'status': False})


# 注册
def register(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    new_user = User(username=username, password=password)
    try:
        new_user.save()
        request.session['uid'] = new_user.id
        request.session['username'] = new_user.username
        return JsonResponse({'ok': True})
    except IntegrityError:
        return JsonResponse({'ok': False, 'msg': '用户名已被使用'})
    except:
        return JsonResponse({'ok': False, 'msg': '服务器繁忙'})


# 登录
def login(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    user = User.objects.filter(username=username, password=password)
    if len(user) == 1:
        request.session['uid'] = user[0].id
        request.session['username'] = user[0].username
        return JsonResponse({'ok': True, 'username': user[0].username})
    else:
        return JsonResponse({'ok': False, 'msg': '用户名或密码错误'})


# 退出
def logout(request):
    request.session.clear()
    return JsonResponse({'ok': True})
