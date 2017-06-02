# coding=utf-8
import json

from django.http import JsonResponse

from stock.data.stock_data import StockData
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
    stock_index = StockData().get_index()
    result = {
        'base': [
            {'name': '沪深300', 'stocks': stock_index[stock_index.index < 2000].index.values.tolist()},
            {'name': '中小板', 'stocks': stock_index[(stock_index.index >= 2000) & (stock_index.index < 3000)].index.values.tolist()},
            {'name': '创业板', 'stocks': stock_index[stock_index.index >= 300000].index.values.tolist()},
        ],
        'industries': [{'id': int(id), 'name': row['name'], 'stocks': json.loads(row['stocks'])} for id, row in StockData().get_industries().iterrows()],
        'custom': []
    }
    if 'uid' in request.session:
        uid = request.session['uid']
        result['custom'] = [{'id': pool.id, 'name': pool.name, 'stocks': json.loads(pool.stock_list)} for pool in StockPool.objects.filter(uid=uid)]
    return JsonResponse(result)


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
