# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import time
from datetime import datetime, timedelta

import pandas
from django.http import HttpResponse, JsonResponse

from dwebsocket import accept_websocket
from stock.data import qtshare
from stock.data.stock_data import StockData


# Create your views here.


def get_index(request):
    index = StockData().get_index()
    min_date, max_date = StockData().get_date_range()
    return HttpResponse(json.dumps({'min': str(min_date), 'max': str(max_date),
                                    'index': {int(code): row.to_dict() for code, row in index.iterrows()}}))


def market(request):
    start = time.time()
    result = {
        'volumes': [],
        'top_surge': [],
        'top_decline': [],
        'top_industries': [],
        'last_industries': []
    }
    date = datetime.strptime(request.GET['date'], '%Y-%m-%d').date()
    index = StockData().get_index()
    info = StockData().get_info(date=date, date_start=date - timedelta(days=14))

    dates = info['date'].drop_duplicates()
    for row in dates:
        result['volumes'].append((str(row), int(info[info['date'] == row]['volume'].sum())))

    info_today = info[info['date'] == date].dropna()
    for i in range(1, 14):
        info_yesterday = info[info['date'] == date - timedelta(days=i)]
        if len(info_yesterday) > 0:
            break
    if len(info_today) == 0 or len(info_yesterday) == 0:
        return JsonResponse({'ok': False, 'msg': '当天无股票数据，请更换日期'})

    info_today['name'] = index['name']
    info_today['adjclose_last'] = info_yesterday['adjclose']
    info_today['raising'] = (info_today.adjclose - info_today.adjclose_last) / info_today.adjclose_last

    info_today = info_today.sort_values('raising', ascending=False)

    for code, stk in info_today[info_today['raising'] >= 0].iloc[:20].iterrows():
        result['top_surge'].append(
            {'code': int(code), 'name': stk['name'], 'close': stk['close'], 'rate': stk['raising']})
    for code, stk in info_today[info_today['raising'] <= 0].iloc[:-21:-1].iterrows():
        result['top_decline'].append(
            {'code': int(code), 'name': stk['name'], 'close': stk['close'], 'rate': stk['raising']})

    industries = StockData().get_industries()
    industries['total'] = pandas.Series()
    industries['surged'] = pandas.Series()
    industries['declined'] = pandas.Series()
    for index, row in industries.iterrows():
        stk_list = json.loads(row['stocks'])
        stk_info = info_today[info_today.index.isin(stk_list)]
        industries.loc[index, 'total'] = len(stk_info)
        industries.loc[index, 'surged'] = len(stk_info[stk_info['raising'] > 0])
        industries.loc[index, 'declined'] = len(stk_info[stk_info['raising'] < 0])
    industries['rate'] = industries['surged'] / industries['total']
    industries['dec_rate'] = industries['declined'] / industries['total']
    industries = industries.sort_values('rate', ascending=False)
    for _, row in industries[industries['rate'] >= 0].iloc[:10].iterrows():
        result['top_industries'].append(
            {'name': row['name'], 'total': row['total'], 'count': row['surged'], 'rate': row['rate']})
    industries = industries.sort_values('dec_rate', ascending=False)
    for _, row in industries[industries['dec_rate'] >= 0].iloc[:10].iterrows():
        result['last_industries'].append(
            {'name': row['name'], 'total': row['total'], 'count': row['declined'], 'rate': row['dec_rate']})

    result['total'] = len(info_today)
    result['surged'] = len(info_today[info_today.raising > 0])
    result['balanced'] = len(info_today[info_today.raising == 0])
    result['declined'] = len(info_today[info_today.raising < 0])
    return JsonResponse(result)


def stock_list(request):
    date = datetime.strptime(request.GET['date'], '%Y-%m-%d').date()
    info = StockData().get_info(date=date, date_start=date - timedelta(days=1))
    info_today = info[info['date'] == date]
    info_yesterday = info[info['date'] == date - timedelta(days=1)]
    index = StockData().get_index()

    info_today.loc[:, 'name'] = index['name']
    info_today.loc[:, 'close_last'] = info_yesterday['close']
    info_today.loc[:, 'adjclose_last'] = info_yesterday['adjclose']
    info_today.loc[:, 'raising'] = (info_today.adjclose - info_today.adjclose_last) / info_today.adjclose_last

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


def stock_news(request):
    code = int(request.GET.get('code', 0))
    count = int(request.GET.get('count', 10))
    df = qtshare.stock_news(code)
    if len(df) > count:
        df = df[0:count]
    return HttpResponse(json.dumps(df.to_dict(orient='record')))


def stock_predict(request):
    import keras
    from stock.predict_util import lstm

    code = int(request.GET['code'])
    info = StockData().get_info(code=code, limit=90).iloc[::-1]
    data = list(info['close'])

    keras.backend.clear_session()
    model = keras.models.load_model('model.h5')
    new_data = lstm.pure_deal_data(data, 30)
    predict_list = lstm.pure_predict(model, new_data)
    predict_rate = [((1 + predict_list[i]) * data[i] - data[i + 29]) / data[i + 29] for i in range(len(predict_list))]
    real_rate = [(data[i + 30] - data[i + 29]) / data[i + 29] for i in range(len(predict_list) - 1)]
    return JsonResponse({'tomorrow': predict_rate[-1], 'predict': predict_rate[:-1],
                         'real': real_rate, 'dates': list(info[-60:]['date'])})


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
