# coding=utf-8
import json
import traceback
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from dwebsocket import accept_websocket

from trade import backtest_engine
from trade.models import Strategy, BacktestResult


@accept_websocket
def backtest(request):
    if 'uid' in request.session:
        if request.is_websocket():
            uid = request.session['uid']
            strategy_id = request.GET.get('id', 0)
            strategy = Strategy.objects.filter(uid=uid, id=strategy_id)
            if strategy:
                strategy = strategy[0]
            else:
                request.websocket.send(json.dumps({'error': True, 'msg': '策略不存在'}))
                return
            # wait for params
            msg = request.websocket.wait()
            args = json.loads(msg)
            args['code'] = strategy.code
            try:
                result = backtest_engine.run(args, request.websocket)
            except Exception as e:
                request.websocket.send(json.dumps({'error': True, 'msg': repr(e)}))
                traceback.print_exc()
                return
            if result:
                BacktestResult(uid=uid, time=datetime.now(), strategy=strategy_id, parameter=msg,
                               result=json.dumps(result)).save()
        else:
            return HttpResponse('This path accepts WebSocket connections.')
    else:
        return HttpResponse('Access Denied')


def get_history_list(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        histories = BacktestResult.objects.filter(uid=uid).order_by('-time')
        history_list = []
        for his in histories:
            strategy = Strategy.objects.filter(id=his.strategy)
            if not strategy:
                name = '[ 策略已被删除 ]'
            else:
                name = strategy[0].name
            args = json.loads(his.parameter)
            result = json.loads(his.result)
            history_list.append({'id': his.id, 'time': his.time.strftime('%Y-%m-%d %H:%M:%S'), 'strategy_name': name,
                                 'freq': args['frequency'], 'annualized': result['result']['annualized'],
                                 'base_annualized': result['result']['base_annualized']})
        return JsonResponse({'ok': True, 'histories': history_list})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})


def get_history(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        id = request.GET.get('id', None)
        history = BacktestResult.objects.filter(uid=uid, id=id)
        if history:
            return JsonResponse({'ok': True, 'history': list(history.values())[0]})
        else:
            return JsonResponse({'ok': False, 'msg': '回测历史不存在'})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})
