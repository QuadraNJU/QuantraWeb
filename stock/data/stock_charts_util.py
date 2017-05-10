# coding=utf-8
from datetime import datetime
from time import time

from stock.data import stock_util, stock_data


def volume(infos):
    return {'volume': infos.volume.tolist()}

# dif计算花费50+s，需要优化
def macd(infos):
    code = infos.index[0]
    date_start = min(infos.date)
    srt = 12
    lng = 26
    mid = 9
    result = {
        'dif': [],
        'dea': [],
        'macd': [],
    }
    infos = infos.append(stock_data.StockData().get_a_stock_days_before(date_start, code, mid))
    result['dif'] = [stock_util.EMA_n(index, stk.date, srt) - stock_util.EMA_n(index, stk.date, lng) for
                     index, stk in infos.iterrows()]
    result['dea'] = [stock_util.EMA(result['dif'][i: i + mid]) for i in range(0, len(result['dif']) - 9)]
    result['dif'] = result['dif'][0:len(result['dif'])-9]
    result['macd'] = [(result['dif'][i] - result['dea'][i]) * 2 for i in range(0, len(result['dif']))]
    return result
