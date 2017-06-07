# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse

from forum.models import Forum
from django.shortcuts import render

# Create your views here.
def get_list(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        forum = Forum.objects.filter(uid=uid)
        return JsonResponse({'ok':True, 'forums':list(forum.values('id'))})
    else:
        return JsonResponse({'ok':False, 'msg':'帖子不存在'})

def new_Forum(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        _id = request.POST.get('id', 0)
        time = request.POST.get('time', '')
        content = request.POST.get('content', '')
        reply = request.POST.get('reply', '')

        new_model = Forum(uid=uid)
        new_model.uid = _id
        new_model.time = time
        new_model.content = content
        new_model.reply = reply
        try:
            new_model.save()
            return JsonResponse({'ok': True, 'id': new_model.id})
        except:
            return JsonResponse({'ok': False, 'msg': '发帖失败：服务器异常'})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})

def delete(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        _id = request.GET.get('id', 0)
        model = Forum.objects.filter(id=_id, uid = uid)
        if model:
            try:
                model.delete()
                return JsonResponse({'ok': True})
            except:
                return JsonResponse({'ok': False, 'msg': '删除失败：服务器异常'})
        else:
                return JsonResponse({'ok': False, 'msg': '删除失败：帖子不存在'})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})