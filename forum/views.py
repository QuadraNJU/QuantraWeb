# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.http import JsonResponse

from forum.models import Thread
from users.models import User


def __get_username(uid):
    user = User.objects.filter(id=uid)
    if user:
        return user[0].username
    else:
        return '无名用户'


def get_list(request):
    forum = Thread.objects.order_by('-time')
    threads = []
    thread_times = {}
    for thread in forum:
        if thread.reply > 0 and thread.reply not in thread_times:
            thread_times[thread.reply] = thread.time
        if thread.reply == 0:
            if thread.id in thread_times:
                last_reply = thread_times[thread.id]
            else:
                last_reply = thread.time
            threads.append({'id': thread.id, 'time': thread.time.strftime('%Y/%m/%d %H:%M:%S'),
                            'last_reply': last_reply.strftime('%Y/%m/%d %H:%M:%S'),
                            'username': __get_username(thread.uid), 'title': thread.title, 'tag': thread.tag})
    threads = sorted(threads, key=lambda t: t['last_reply'], reverse=True)
    return JsonResponse({'ok': True, 'threads': threads})


def get_thread(request):
    _id = request.GET.get('id', 0)
    thread = Thread.objects.filter(id=_id)
    if thread:
        thread = thread[0]
        replies = []
        for reply in Thread.objects.filter(reply=_id).order_by('time'):
            replies.append({
                'username': __get_username(reply.uid),
                'time': reply.time.strftime('%Y/%m/%d %H:%M:%S'),
                'content': reply.content
            })
        return JsonResponse({'ok': True, 'thread': {
            'username': __get_username(thread.uid),
            'title': thread.title, 'tag': thread.tag, 'content': thread.content,
            'time': thread.time.strftime('%Y/%m/%d %H:%M:%S'),
            'last_reply': replies[-1]['time'] if len(replies) > 0 else thread.time.strftime('%Y/%m/%d %H:%M:%S'),
        }, 'replies': replies})
    else:
        return JsonResponse({'ok': False, 'msg': '帖子不存在'})


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
