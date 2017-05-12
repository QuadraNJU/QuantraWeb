# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import time
from datetime import datetime, timedelta

import tushare as ts
from django.http import HttpResponse
from dwebsocket import accept_websocket

from stock.data import stock_util, stock_charts_util
from stock.data.stock_data import StockData


# Create your views here.
def date_range(request):
    min_date, max_date = StockData().get_date_range()
    return HttpResponse(json.dumps({'min': str(min_date), 'max': str(max_date)}))


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
    print time.time() - start

    dates = info['date'].drop_duplicates()
    for row in dates:
        result['volumes'].append((str(row), int(info[info['date'] == row]['volume'].sum())))
    print time.time() - start

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

    print time.time() - start
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
    for code, row in info_today.iterrows():
        result.append((int(code), row['name'], row['open'], row['high'], row['low'], row['close'], row['close_last'],
                       row['raising'], row['volume']))

    return HttpResponse(json.dumps(result))


def stock(request):
    result = {
        'MA5': [],
        'MA10': [],
        'MA20': [],
        'MA30': [],
        'MA60': [],
    }
    date_start = datetime.strptime(request.GET['date_start'], '%Y-%m-%d').date()
    date_end = datetime.strptime(request.GET['date_end'], '%Y-%m-%d').date()
    code = int(request.GET['code'])

    if date_start > date_end:
        date_start = date_end - timedelta(days=1)
    infos = StockData().get_info(code=code)
    infos = infos[infos.date <= date_end]
    infos = infos[infos.date >= date_start]
    t = get_time()
    result['MA5'] = [stock_util.MA_n(code, line['date'], 5) for index, line in infos.iterrows()]
    result['MA10'] = [stock_util.MA_n(code, line['date'], 10) for index, line in infos.iterrows()]
    result['MA20'] = [stock_util.MA_n(code, line['date'], 20) for index, line in infos.iterrows()]
    result['MA30'] = [stock_util.MA_n(code, line['date'], 30) for index, line in infos.iterrows()]
    result['MA60'] = [stock_util.MA_n(code, line['date'], 60) for index, line in infos.iterrows()]

    return HttpResponse(get_time() - t)


def volume_chart(request):
    date_start = datetime.strptime(request.GET['date_start'], '%Y-%m-%d').date()
    date_end = datetime.strptime(request.GET['date_end'], '%Y-%m-%d').date()
    code = int(request.GET['code'])

    if date_start > date_end:
        date_start = date_end - timedelta(days=1)
    infos = StockData().get_a_stock_with_date_range(date_start=date_start, date_end=date_end, code=code)

    result = stock_charts_util.volume(infos)
    return HttpResponse(json.dumps(result))


def macd_chart(request):
    date_start = datetime.strptime(request.GET['date_start'], '%Y-%m-%d').date()
    date_end = datetime.strptime(request.GET['date_end'], '%Y-%m-%d').date()
    code = int(request.GET['code'])

    if date_start > date_end:
        date_start = date_end - timedelta(days=1)
    infos = StockData().get_a_stock_with_date_range(date_start=date_start, date_end=date_end, code=code)

    macd = stock_charts_util.macd(infos)
    return HttpResponse(json.dumps(macd))


def kdj_chart(request):
    date_start = datetime.strptime(request.GET['date_start'], '%Y-%m-%d').date()
    date_end = datetime.strptime(request.GET['date_end'], '%Y-%m-%d').date()
    code = int(request.GET['code'])

    if date_start > date_end:
        date_start = date_end - timedelta(days=1)
    infos = StockData().get_a_stock_with_date_range(date_start=date_start, date_end=date_end, code=code)
    kdj = stock_charts_util.kdj(infos)

    return HttpResponse(json.dumps(kdj))


def boll_chart(request):
    date_start = datetime.strptime(request.GET['date_start'], '%Y-%m-%d').date()
    date_end = datetime.strptime(request.GET['date_end'], '%Y-%m-%d').date()
    code = int(request.GET['code'])

    if date_start > date_end:
        date_start = date_end - timedelta(days=1)
    infos = StockData().get_a_stock_with_date_range(date_start=date_start, date_end=date_end, code=code)
    boll = stock_charts_util.boll(infos)

    return HttpResponse(json.dumps(boll))


def psy_chart(request):
    date_start = datetime.strptime(request.GET['date_start'], '%Y-%m-%d').date()
    date_end = datetime.strptime(request.GET['date_end'], '%Y-%m-%d').date()
    code = int(request.GET['code'])

    if date_start > date_end:
        date_start = date_end - timedelta(days=1)
    infos = StockData().get_a_stock_with_date_range(date_start=date_start, date_end=date_end, code=code)
    psy = stock_charts_util.psy(infos)

    return HttpResponse(json.dumps(psy))


@accept_websocket
def realtime_price(request):
    if request.is_websocket():
        while not request.websocket.closed:
            if request.websocket.has_messages():
                msg = request.websocket.read()
                if msg is None:
                    break
            result = []
            df = ts.get_today_ticks('000001')
            print ''
            today = datetime.now().strftime('%Y-%m-%d')
            current_minute = ''
            for _, row in df.iloc[::-1].iterrows():
                minute = row['time'][:5]
                if minute != current_minute:
                    current_minute = minute
                    result.append((today + ' ' + minute, row['price']))
            request.websocket.send(json.dumps(result))
            time.sleep(10)
    else:
        return HttpResponse('This path accepts WebSocket connections.')
