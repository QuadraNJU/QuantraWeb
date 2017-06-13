var QuantraTemplate = '# coding=utf-8\n\
import pandas as pd\n\
import numpy as np\n\
import stock.data.qtshare as qts\n\
\n\
# 可在此处编写策略初始化相关逻辑\n\
\n\
def handle(account):\n\
    # 在此处编写每个持有期的处理逻辑\n\
    pass\n\
';

var QuantraSnippets = [
    {
        'name': '获取当前策略的参数列表',
        'code': 'account.params'
    },
    {
        'name': '获取当前账户的可用资金',
        'code': 'account.cash'
    },
    {
        'name': '获取上一周期结束后的总资金',
        'code': 'account.portfolio'
    },
    {
        'name': '获取当前持仓的股票列表',
        'code': 'account.sec_pos[]'
    },
    {
        'name': '获取当天所有股票的交易价格',
        'code': 'account.price[]'
    },
    {
        'name': '获取当天可交易的所有股票列表',
        'code': 'account.get_stocks()'
    },
    {
        'name': '获取当天所有股票在一段时间内的历史数据',
        'code': 'account.get_history(\'attr\', days)'
    },
    {
        'name': '对某个股票发起买入或卖出交易',
        'code': 'account.trade(stock, target)'
    },
    {
        'name': '获取所选股票池内所有股票在所有日期上的数据',
        'code': 'account.universe_data'
    },
    {
        'name': '获取所选股票池内所有股票在当前日期上的数据',
        'code': 'account.today_data'
    }
];