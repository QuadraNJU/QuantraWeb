from datetime import datetime
from time import time

import pandas as pd

from stock import views
from stock.data.stock_data import StockData

stock_infos = StockData().get_by_date('2015-4-10')
stock_infos_last = StockData().get_last_date_info('2015-4-10')
stock_infos['close_last'] = stock_infos_last['close']

stock_infos['other_rate'] = (stock_infos.open - stock_infos.close) / stock_infos.close_last
print stock_infos.sort_index()
