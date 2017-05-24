# coding=utf-8
from django.http import JsonResponse
from django.db import IntegrityError
from trade.models import Strategy


def createStrategy(request):
    if 'uid' in request.COOKIES:
        uid = request.COOKIES['uid']
        name = request.POST.get('name', None)
        code = request.POST.get('code', None)
        parameters = request.POST.get('parameters', None)
        is_public = request.POST.get('is_public', None)
        new_strategy = Strategy(uid=uid, name=name, code=code, parameters=parameters, is_public=is_public)
        try:
            new_strategy.save()
            return JsonResponse({'ok': True})
        except IntegrityError:
            return JsonResponse({'ok': False, 'msg': '参数未填写完整，请重新填写'})
        except:
            return JsonResponse({'ok': False, 'msg': '服务器繁忙'})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})


def readStrategy(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        id = request.POST.get('id', None)
        strategy = Strategy.objects.filter(uid=uid)
        if id:
            strategy = strategy.filter(id=id)
        strategy = list(strategy.values('id', 'uid', 'name', 'code', 'parameters', 'is_public'))
        if strategy:
            return JsonResponse({'ok': True, 'strategy': strategy})
        else:
            return JsonResponse({'ok': False, 'msg': '访问了不属于该用户的策略，请重试'})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})


def updateStrategyById(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        id = request.POST.get('id', None)
        try:
            strategy = Strategy.objects.filter(id=id, uid=uid)
            if strategy:
                code = request.POST.get('code', strategy[0].code)
                parameters = request.POST.get('parameters', strategy[0].parameters)
                is_public = request.POST.get('is_public', strategy[0].is_public)
                strategy.update(parameters=parameters, code=code, is_public=is_public)
                return JsonResponse({'ok': True})
            else:
                return JsonResponse({'ok': False, 'msg': '访问了不属于该用户的策略，请重试'})
        except:
            return JsonResponse({'ok': False, 'msg': '获取策略失败，无法更新'})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})


def deleteStrategyById(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        id = request.POST.get('id', None)
        strategy = Strategy.objects.filter(id=id, uid=uid)
        if strategy:
            (success, _) = strategy.delete()
            response = {'ok': success}
            if not success:
                response['msg'] = '删除策略过程中出现异常，请刷新'
            return JsonResponse(response)
        else:
            return JsonResponse({'ok': False, 'msg': '访问了不属于该用户的策略，请重试'})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})
