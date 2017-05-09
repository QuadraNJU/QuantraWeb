# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd

from stock.data.stock_data import StockData


# Create your views here.
def get_latest(request):
    df = StockData().get_by_date('2017-03-01')
    return HttpResponse(df.to_json(orient='records'))


def market(request):
    ctx = {'title_name': 'Market'}
    date = request.GET['date']
    stock_infos = StockData().get_by_date(date)
    stock_infos_last = StockData().get_last_date_info(date)
    stock_infos['close_last'] = stock_infos_last['close']
    stock_infos['adjclose_last'] = stock_infos_last['adjclose']
    stock_infos['other_rate'] = (stock_infos.open - stock_infos.close) / stock_infos.close_last
    stock_infos['raising'] = (stock_infos.adjclose_last - stock_infos.adjclose) / stock_infos.adjclose_last
    # 涨跌停
    surged_limit = stock_infos[stock_infos.raising >= 0.1]
    surged_over_five_per = stock_infos[stock_infos.raising > 0.05]
    decline_limit = stock_infos[stock_infos.raising <= -0.1]
    decline_over_five_per = stock_infos[stock_infos.raising < -0.05]
    other_over_five_per = stock_infos[stock_infos.other_rate > 0.05]
    other_below_neg_five_per = stock_infos[stock_infos.other_rate < -0.05]

    ctx['total'] = len(stock_infos)
    ctx['surged'] = len(stock_infos[stock_infos.raising > 0])
    ctx['balanced'] = len(stock_infos[stock_infos.raising == 0])
    ctx['declined'] = len(stock_infos[stock_infos.raising < 0])
    return HttpResponse(json.dumps(ctx))
