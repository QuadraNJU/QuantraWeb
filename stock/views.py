# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse

from stock.data.stock_data import StockData


# Create your views here.
def get_latest(request):
    df = StockData().get_by_date('2017-03-01')
    return HttpResponse(df.to_json(orient='records'))
