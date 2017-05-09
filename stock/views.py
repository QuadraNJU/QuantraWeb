# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

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

    date = request.GET['date']
    index = StockData().get_index()
    info = StockData().get_by_date(date)
    info_yesterday = StockData().get_yesterday_info(date)

    info['name'] = index['name']
    info['adjclose_last'] = info_yesterday['adjclose']
    info['raising'] = (info.adjclose_last - info.adjclose) / info.adjclose_last

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
