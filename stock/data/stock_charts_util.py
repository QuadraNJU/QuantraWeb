# coding=utf-8
from datetime import datetime
from time import time

from numpy import mean, std

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
    result['dif'] = result['dif'][0:len(result['dif']) - 9]
    result['macd'] = [(result['dif'][i] - result['dea'][i]) * 2 for i in range(0, len(result['dif']))]
    return result


def kdj(infos):
    code = infos.index[0]
    date_start = min(infos.date)
    n = 9
    m = 3
    rsv = []
    result = {
        'k': [],
        'd': [],
        'j': [],
    }
    infos = infos.append(stock_data.StockData().get_a_stock_days_before(date_start, code, n + 2 * m))
    for i in range(0, len(infos) - n):
        llv = min(infos.low[i: i + n])
        hhv = max(infos.high[i: i + n])
        rsv.append((infos.close.tolist()[i] - llv) / (hhv - llv) * 100)
    result['k'] = [mean(rsv[i - m: i]) for i in range(m, len(rsv))]
    result['d'] = [mean(result['k'][i - m: i]) for i in range(m, len(result['k']))]
    result['k'] = result['k'][0: len(result['d'])]
    result['j'] = [3 * result['k'][i] - 2 * result['d'][i] for i in range(0, len(result['k']))]
    return result


def boll(infos):
    length = len(infos)
    code = infos.index[0]
    date_start = min(infos.date)
    n = 20
    result = {'boll': [stock_util.MA_n(index, stk.date, n) for index, stk in infos.iterrows()]}
    infos = infos.append(stock_data.StockData().get_a_stock_days_before(date_start, code, n))
    __std = [std(infos.close[i: i + n]) for i in range(0, length)]
    result['upper'] = [result['boll'][i] + 2 * __std[i] for i in range(0, length)]
    result['lower'] = [result['boll'][i] - 2 * __std[i] for i in range(0, length)]
    return result


def psy(infos):
    length = len(infos)
    n = 12
    code = infos.index[0]
    date_start = min(infos.date)
    infos = infos.append(stock_data.StockData().get_a_stock_days_before(date_start, code, n + 1))
    day_raise = (infos[0: len(infos) - 1].close - infos[1: len(infos)].close).tolist()
    raise_count = [len(filter(lambda x: x > 0, day_raise[i: i+n])) for i in range(0, length)]
    return {'psy': [count * 1.0 / n * 100 for count in raise_count]}
