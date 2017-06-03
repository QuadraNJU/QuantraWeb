# coding=utf-8
import json

from django.http import JsonResponse

from stock.data.stock_data import StockData
from trade.models import StockPool


def updatePool(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        id = request.POST.get('id', None)
        name = request.POST.get('name', '')
        stock_list = request.POST.get('stocks', '[]')
        if id is None:
            new_pool = StockPool(uid=uid)
        else:
            new_pool = StockPool.objects.filter(id=id, uid=uid)
            if new_pool:
                new_pool = new_pool[0]
            else:
                new_pool = StockPool(uid=uid)
        new_pool.name = name
        new_pool.stock_list = stock_list
        try:
            new_pool.save()
            return JsonResponse({'ok': True})
        except:
            return JsonResponse({'ok': False, 'msg': '服务器异常'})
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


def getPoolById(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        id = request.GET.get('id', None)
        pool = StockPool.objects.filter(id=id, uid=uid)
        if pool:
            return JsonResponse({'ok': True, 'name': pool[0].name, 'stocks': json.loads(pool[0].stock_list)})
        else:
            return JsonResponse({'ok': False, 'msg': '股票池不存在'})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})


def deletePoolById(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        id = request.GET.get('id', None)
        pool = StockPool.objects.filter(id=id, uid=uid)
        if pool:
            (success, _) = pool.delete()
            response = {'ok': success}
            if not success:
                response['msg'] = '服务器异常'
            return JsonResponse(response)
        else:
            return JsonResponse({'ok': False, 'msg': '股票池不存在'})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})
