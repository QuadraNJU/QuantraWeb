# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import time
from datetime import datetime, timedelta

import keras
from django.http import HttpResponse, JsonResponse

from dwebsocket import accept_websocket
from stock.data import qtshare
from stock.data.stock_data import StockData


# Create your views here.
from stock.lstm_util import predict_util


def get_index(request):
    index = StockData().get_index()
    min_date, max_date = StockData().get_date_range()
    return HttpResponse(json.dumps({'min': str(min_date), 'max': str(max_date),
                                    'index': {int(code): row.to_dict() for code, row in index.iterrows()}}))


def market(request):
    start = time.time()
    result = {
        'volumes': [],
        'surged_limit': [],
        'surged_over_five_per': [],
        'decline_limit': [],
        'decline_over_five_per': [],
    }
    date = datetime.strptime(request.GET['date'], '%Y-%m-%d').date()
    index = StockData().get_index()
    info = StockData().get_info(date=date, date_start=date - timedelta(days=14))

    dates = info['date'].drop_duplicates()
    for row in dates:
        result['volumes'].append((str(row), int(info[info['date'] == row]['volume'].sum())))

    info_today = info[info['date'] == date]
    info_yesterday = info[info['date'] == date - timedelta(days=1)]

    info_today['name'] = index['name']
    info_today['adjclose_last'] = info_yesterday['adjclose']
    info_today['raising'] = (info_today.adjclose - info_today.adjclose_last) / info_today.adjclose_last

    for code, stk in info_today.iterrows():
        line = {'code': int(code), 'name': stk['name'], 'close': stk['close'], 'rate': stk['raising']}
        if stk['raising'] >= 0.1:
            result['surged_limit'].append(line)
        elif stk['raising'] > 0.05:
            result['surged_over_five_per'].append(line)
        elif stk['raising'] <= -0.1:
            result['decline_limit'].append(line)
        elif stk['raising'] < -0.05:
            result['decline_over_five_per'].append(line)

    result['total'] = len(info_today)
    result['surged'] = len(info_today[info_today.raising > 0])
    result['balanced'] = len(info_today[info_today.raising == 0])
    result['declined'] = len(info_today[info_today.raising < 0])
    return HttpResponse(json.dumps(result))


def stock_list(request):
    date = datetime.strptime(request.GET['date'], '%Y-%m-%d').date()
    info = StockData().get_info(date=date, date_start=date - timedelta(days=1))
    info_today = info[info['date'] == date]
    info_yesterday = info[info['date'] == date - timedelta(days=1)]
    index = StockData().get_index()

    info_today['name'] = index['name']
    info_today['close_last'] = info_yesterday['close']
    info_today['adjclose_last'] = info_yesterday['adjclose']
    info_today['raising'] = (info_today.adjclose - info_today.adjclose_last) / info_today.adjclose_last

    result = []
    for code, row in info_today.dropna().iterrows():
        result.append((int(code), row['name'], row['open'], row['high'], row['low'], row['close'], row['close_last'],
                       row['raising'], row['volume']))

    return HttpResponse(json.dumps(result))


def stock(request):
    result = {'dates': [], 'data': [], 'volume': []}
    code = int(request.GET['code'])
    infos = StockData().get_info(code=code, limit=500)
    index = StockData().get_index()
    result['name'] = index['name'][code]
    for code, row in infos.iloc[::-1].dropna().iterrows():
        result['dates'].append(str(row['date']))
        result['data'].append((row['open'], row['close'], row['low'], row['high']))
        result['volume'].append(row['volume'])
    return HttpResponse(json.dumps(result))


def stock_predict(request):
    predict_correct = 0
    code = int(request.GET['code'])
    infos = list(StockData().get_info(code=code, limit=100)['close'])
    window = infos[0]

    model = keras.models.load_model('model.h5')
    predict_list, real_list = predict_util.data_predict(infos, model)
    keras.backend.clear_session()
    predict_list = [(i + 1) * window for i in predict_list]
    real_list = [(i + 1) * window for i in real_list]

    for i in range(len(predict_list) - 1):
        if predict_list[i+1] - predict_list[i] < 0 and real_list[i+1] - real_list[i] < 0:
            predict_correct += 1
        elif predict_list[i+1] - predict_list[i] > 0 and real_list[i+1] - real_list[i] > 0:
            predict_correct += 1

    return JsonResponse({'result': float(predict_correct) / len(predict_list)})


def build_model(request):
    date_start, date_end = StockData().get_date_range()
    train_data = list(StockData().get_info(code=1)['close'])
    model = predict_util.build_model(train_data)
    model.save('model.h5')
    return JsonResponse({'ok': True})


@accept_websocket
def realtime_list(request):
    if request.is_websocket():
        while not request.websocket.closed:
            if request.websocket.has_messages():
                msg = request.websocket.read()
                if msg is None:
                    break
            result = []
            start = time.time()
            df = qtshare.today_list()
            for _, row in df.iterrows():
                if row['volume'] > 0:
                    result.append((row['code'], row['name'], row['open'], row['high'], row['low'], row['price'],
                                   row['yest_close'], row['rate'], row['volume'], row['turn_over']))
            request.websocket.send(json.dumps(result))
            time.sleep(10)
    else:
        return HttpResponse('This path accepts WebSocket connections.')


@accept_websocket
def realtime_price(request):
    if request.is_websocket():
        while not request.websocket.closed:
            if request.websocket.has_messages():
                msg = request.websocket.read()
                if msg is None:
                    break
            result = {'ticks': [], 'prices': [], 'volumes': []}
            try:
                df = qtshare.today_ticks(int(request.GET['code']))
                for _, row in df.iterrows():
                    result['ticks'].append(row['tick'])
                    result['prices'].append(row['price'])
                    result['volumes'].append(row['volume'])
            except:
                pass
            result['quotes'] = qtshare.today_quotes(int(request.GET['code'])).to_dict()
            request.websocket.send(json.dumps(result))
            time.sleep(10)
    else:
        return HttpResponse('This path accepts WebSocket connections.')
