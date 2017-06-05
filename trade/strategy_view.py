# coding=utf-8
from django.http import JsonResponse

from trade.models import Strategy


def get_list(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        strategy = Strategy.objects.filter(uid=uid)
        return JsonResponse({'ok': True, 'strategies': list(strategy.values('id', 'name'))})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})


def get_detail(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        id = request.GET.get('id', None)
        strategy = Strategy.objects.filter(uid=uid, id=id)
        if strategy:
            return JsonResponse({'ok': True, 'detail': list(strategy.values())[0]})
        else:
            return JsonResponse({'ok': False, 'msg': '策略不存在'})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})


def update(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        _id = request.POST.get('id', 0)

        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        code = request.POST.get('code', '')
        parameters = request.POST.get('parameters', '')
        is_public = request.POST.get('is_public', 'false')

        if int(_id) <= 0:
            new_model = Strategy(uid=uid)
        else:
            new_model = Strategy.objects.filter(id=_id, uid=uid)
            if new_model:
                new_model = new_model[0]
            else:
                return JsonResponse({'ok': False, 'msg': '更新失败：策略不存在'})
        new_model.name = name
        new_model.description = description
        new_model.code = code
        new_model.parameters = parameters
        new_model.is_public = (is_public == 'true')
        try:
            new_model.save()
            return JsonResponse({'ok': True, 'id': new_model.id})
        except:
            return JsonResponse({'ok': False, 'msg': '更新失败：服务器异常'})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})


def delete(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        _id = request.GET.get('id', 0)
        model = Strategy.objects.filter(id=_id, uid=uid)
        if model:
            try:
                model.delete()
                return JsonResponse({'ok': True})
            except:
                return JsonResponse({'ok': False, 'msg': '删除失败：服务器异常'})
        else:
            return JsonResponse({'ok': False, 'msg': '删除失败：策略不存在'})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})
