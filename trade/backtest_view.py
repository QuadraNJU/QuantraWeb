# coding=utf-8
import json

from django.http import HttpResponse
from dwebsocket import accept_websocket

from trade import backtest_engine
from trade.models import Strategy


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
            # wait for params
            msg = request.websocket.wait()
            args = json.loads(msg)
            args['code'] = strategy.code
            backtest_engine.run(args, request.websocket)
        else:
            return HttpResponse('This path accepts WebSocket connections.')
    else:
        return HttpResponse('Access Denied')
