from numpy import mean, NaN

from stock.data.stock_data import StockData


def MA_n(code, date, n):
    infos = StockData().get_a_stock_days_before(date, code, n)
    if len(infos) == n:
        return mean(infos.close)
    else:
        return NaN


def EMA(lis):
    alpha = 2.0 / (len(lis) + 1)
    _sum = 0
    for i in range(0, len(lis) - 1):
        _sum += alpha ** i * lis[i]
    return _sum * alpha


def EMA_n(code, date, n):
    infos = StockData().get_a_stock_days_before(date, code, n)
    if len(infos) == n:
        return EMA(infos.close.tolist())
    else:
        return NaN
