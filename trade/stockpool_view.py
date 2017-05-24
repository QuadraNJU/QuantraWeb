# coding=utf-8

from django.http import JsonResponse

from trade.models import StockPool


def createPool(request):
    if 'uid' in request.COOKIES:
        uid = request.COOKIES['uid']
        name = request.POST.get('name', None)
        stock_list = request.POST.get('stock_list', None)
        new_pool = StockPool(uid=uid, name=name, stock_list=stock_list)
        try:
            new_pool.save()
            return JsonResponse({'ok': True})
        except:
            return JsonResponse({'ok': False, 'msg': '服务器繁忙'})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})


def readPool(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        id = request.POST.get('id', None)
        pool = StockPool.objects.filter(uid=uid)
        if id:
            pool = pool.filter(id=id)
        pool = list(pool.values('id', 'uid', 'name', 'stock_list'))
        if pool:
            return JsonResponse({'ok': True, 'pool_list': pool})
        else:
            return JsonResponse({'ok': False, 'msg': '获取股票池失败'})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})


def updatePoolById(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        id = request.POST.get('id', None)
        try:
            pool = StockPool.objects.filter(id=id, uid=uid)
            if pool:
                stock_list = request.POST.get('stock_list', pool[0].stock_list)
                pool.update(stock_list=stock_list)
                return JsonResponse({'ok': True})
            else:
                return JsonResponse({'ok': False, 'msg': '访问了不属于该用户的股票池，请重试'})
        except:
            return JsonResponse({'ok': False, 'msg': '获取股票池失败，无法更新'})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})


def deletePoolById(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        id = request.POST.get('id', None)
        pool = StockPool.objects.filter(id=id, uid=uid)
        if pool:
            (success, _) = pool.delete()
            response = {'ok': success}
            if not success:
                response['msg'] = '删除股票池过程中出现异常，请刷新'
            return JsonResponse(response)
        else:
            return JsonResponse({'ok': False, 'msg': '访问了不属于该用户的股票池，请重试'})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})
