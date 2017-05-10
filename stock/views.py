# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import datetime, timedelta

from django.http import HttpResponse

from stock.data.stock_data import StockData


# Create your views here.
def market(request):
    result = {
        'surged_limit': [],
        'surged_over_five_per': [],
        'decline_limit': [],
        'decline_over_five_per': [],
    }
    date = datetime.strptime(request.GET['date'], '%Y-%m-%d')
    index = StockData().get_index()
    info = StockData().get_by_date(date)
    info_yesterday = StockData().get_yesterday_info(date)

    info['name'] = index['name']
    info['adjclose_last'] = info_yesterday['adjclose']
    info['raising'] = (info.adjclose - info.adjclose_last) / info.adjclose_last

    for code, stk in info.iterrows():
        line = {'code': int(code), 'name': stk['name'], 'close': stk['close'], 'rate': stk['raising']}
        if stk['raising'] >= 0.1:
            result['surged_limit'].append(line)
        elif stk['raising'] > 0.05:
            result['surged_over_five_per'].append(line)
        elif stk['raising'] <= -0.1:
            result['decline_limit'].append(line)
        elif stk['raising'] < -0.05:
            result['decline_over_five_per'].append(line)

    result['total'] = len(info)
    result['surged'] = len(info[info.raising > 0])
    result['balanced'] = len(info[info.raising == 0])
    result['declined'] = len(info[info.raising < 0])

    return HttpResponse(json.dumps(result))


def stock_list(request):
    date = datetime.strptime(request.GET['date'], '%Y-%m-%d')
    info = StockData().get_by_date(date)
    info_yesterday = StockData().get_yesterday_info(date)
    index = StockData().get_index()

    info['code'] = info.index
    info['name'] = index['name']
    info['close_last'] = info_yesterday['close']
    info['adjclose_last'] = info_yesterday['adjclose']
    info['raising'] = (info.adjclose - info.adjclose_last) / info.adjclose_last

    return HttpResponse(json.dumps(
        info[['code', 'name', 'raising', 'open', 'high', 'low', 'close', 'volume', 'close_last']].to_dict(
            orient='records'))
    )


def stock(request):
    result = {
        'MA5': [],
        'MA10': [],
        'MA20': [],
        'MA30': [],
        'MA60': [],
    }
    date_start = datetime.strptime(request.GET['date_start'], '%Y-%m-%d')
    date_end = datetime.strptime(request.GET['date_end'], '%Y-%m-%d')
    code = int(request.GET['code'])

    if date_start > date_end:
        date_start = date_end - timedelta(days=1)
    info = StockData().get_info(target_code=code, target_date=date_end)
    info_5_days_before = StockData().get_days_before(date_end, 5)
    info_5_days_before = info_5_days_before[info_5_days_before.index == code]

    result['open'] = float(info_5_days_before['open'])
    result['high'] = float(info_5_days_before['high'])
    result['low'] = float(info_5_days_before['low'])
    result['close'] = float(info_5_days_before['close'])

    return HttpResponse(json.dumps(result))
