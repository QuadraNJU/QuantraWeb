# coding=utf-8
import imp
import json
import time
from datetime import datetime

import numpy

from stock.data.stock_data import StockData


def calc_alpha(_annualized_earn_rate, _base_earn_rate, _beta, _risk_free_interest_rate=0.0175):
    return (_annualized_earn_rate - _risk_free_interest_rate) \
           - _beta * numpy.floor(numpy.mean(_base_earn_rate) - _risk_free_interest_rate)


def calc_beta(_daily_earn_rate, _base_earn_rate):
    n = len(_base_earn_rate)
    if n == 1:
        return 0
    cov = 0
    mean_strategy = numpy.mean(_daily_earn_rate)
    mean_base = numpy.mean(_base_earn_rate)
    for j in range(0, n):
        cov += (_daily_earn_rate[j] - mean_strategy) * (_base_earn_rate[j] - mean_base)
    cov = 1.0 / (n - 1) * cov
    return cov / numpy.var(_base_earn_rate)


def get_date(str):
    return datetime.strptime(str, '%Y-%m-%d').date()


class Account:
    def __init__(self, params, universe, capital):
        self.params = params
        self.cash = self.portfolio = capital
        self.date_index = 0
        self.universe_data = stock_data[stock_data['code'].isin(universe)]
        self.stocks = {}
        self.sec_pos = {}
        self.ref_price = {}
        self.close_price = {}

    def set_date_index(self, date_index):
        self.date_index = date_index
        self.stocks = self.universe_data[self.universe_data['date'] == trade_days[self.date_index]]
        for index, info in self.stocks.iterrows():
            self.ref_price[info['code']] = info['open']  # 今日开盘价
            self.close_price[info['code']] = info['close']  # 今日收盘价
        for stk in self.sec_pos.keys():
            if self.sec_pos[stk] <= 0:
                del self.sec_pos[stk]

    def get_history(self, attr, days):
        if stock_data[attr].empty:
            return None
        result = {}
        for index, _info in self.stocks.iterrows():
            if stock_data.loc[index + days - 1]['code'] == _info['code']:
                result[_info['code']] = stock_data[attr][index:index + days].tolist()
        return result

    def trade(self, stock, target):
        if target < 0 or not self.ref_price[stock]:
            return
        if stock in self.sec_pos:
            curr_amount = self.sec_pos[stock]
        else:
            curr_amount = 0
        diff_amount = target - curr_amount  # 大于0买入，小于0卖出
        new_cash = self.cash - diff_amount * self.ref_price[stock]
        if new_cash < 0:  # 拒绝交易
            return
        self.cash = new_cash
        self.sec_pos[stock] = target


def run(args, ws):
    # load args
    start_date = args['start_date']
    end_date = args['end_date']
    universe = args['universe']
    frequency = int(args['frequency'])
    capital = 100000000
    # load data
    global stock_data
    stock_data = StockData().get_info(date=end_date, date_start=start_date).reset_index()
    global trade_days
    trade_days = stock_data['date'].drop_duplicates().tolist()

    # load dates
    start_date_index = end_date_index = -1
    for i in range(0, len(trade_days)):
        if end_date_index == -1 and trade_days[i] <= get_date(end_date):
            end_date_index = i
        if start_date_index == -1 and trade_days[i] <= get_date(start_date):
            start_date_index = i
    if start_date_index == -1:
        start_date_index = len(trade_days) - 1
    if end_date_index == -1:
        end_date_index = 0
    if start_date_index <= end_date_index:
        ws.send(json.dumps({'error': True, 'msg': '选中日期范围内不包含交易日，请重新选择'}))
        return

    # init strategy and account
    handler = imp.new_module('handler')
    exec args['code'] in handler.__dict__
    account = Account(args['params'], universe, capital)

    daily_earn_rate = []
    base_earn_rate = []
    drawdown = []
    win_times = 0
    history_max_value = 0
    for i in range(start_date_index, end_date_index, -frequency):
        account.set_date_index(i)
        handler.handle(account)
        # portofolio
        new_portfolio = account.cash
        if history_max_value < account.portfolio:
            history_max_value = account.portfolio
        for stk in account.sec_pos:
            new_portfolio += account.sec_pos[stk] * account.close_price[stk]
        account.portfolio = new_portfolio
        # earning rate
        earn_rate = (new_portfolio - capital) / capital
        daily_earn_rate.append(earn_rate)
        # base earning rate
        if i == start_date_index:
            base_stock_price = numpy.mean(account.ref_price.values())
        today_base_earn_rate = (numpy.mean(account.close_price.values()) - base_stock_price) / base_stock_price
        base_earn_rate.append(today_base_earn_rate)
        # update win times
        if earn_rate > today_base_earn_rate:
            win_times += 1
        # Max Drawdown
        drawdown.append(1 - new_portfolio / history_max_value)
        # update progress
        progress = int((start_date_index - i) * 100.0 / (start_date_index - end_date_index))
        info = {'progress': progress, 'date': trade_days[i].strftime('%Y-%m-%d'), 'cash': account.cash,
                'earn_rate': earn_rate, 'base_earn_rate': today_base_earn_rate}
        ws.send(json.dumps(info))

    annualized = daily_earn_rate[-1] / (start_date_index - end_date_index + 1) * 250
    base_annualized = base_earn_rate[-1] / (start_date_index - end_date_index + 1) * 250
    win_rate = win_times * 1.0 / len(daily_earn_rate)
    sharp = (annualized - 0.0175) / numpy.std(daily_earn_rate)
    beta = calc_beta(daily_earn_rate, base_earn_rate)
    alpha = calc_alpha(annualized, base_earn_rate, beta)
    max_drawdown = max(drawdown)

    result = {'success': True, 'annualized': annualized, 'max_drawdown': max_drawdown,
              'base_annualized': base_annualized, 'win_rate': win_rate, 'sharp': sharp, 'beta': beta, 'alpha': alpha}
    ws.send(json.dumps(result))
