# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.http import JsonResponse

from forum.models import Thread
# Create your views here.
from users.models import User


def get_list(request):
    forum = Thread.objects.order_by('-time')
    threads = []
    thread_times = {}
    for thread in forum:
        if thread.reply > 0 and thread.reply not in thread_times:
            thread_times[thread.reply] = thread.time
        if thread.reply == 0:
            user = User.objects.filter(id=thread.uid)
            if user:
                username = user[0].username
            else:
                username = '无名用户'
            if thread.id in thread_times:
                last_reply = thread_times[thread.id]
            else:
                last_reply = thread.time
            threads.append({'id': thread.id, 'time': thread.time, 'last_reply': last_reply,
                            'username': username, 'title': thread.title, 'tag': thread.tag})
    return JsonResponse({'ok': True, 'threads': threads})


def new_thread(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        tag = request.POST.get('tag', '')
        reply = request.POST.get('reply', 0)

        new_model = Thread(uid=uid, time=datetime.now(), title=title, content=content, tag=tag, reply=reply)
        try:
            new_model.save()
            return JsonResponse({'ok': True, 'id': new_model.id})
        except:
            return JsonResponse({'ok': False, 'msg': '发帖失败：服务器异常'})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})


def delete_thread(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        _id = request.GET.get('id', 0)
        model = Thread.objects.filter(id=_id, uid=uid)
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
