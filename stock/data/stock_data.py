import json

import MySQLdb
import pandas as pd
from datetime import timedelta, datetime


class StockData:
    def __conn(self):
        config = json.load(open('global_config.json'))
        if config['db']:
            return MySQLdb.connect(host=config['db']['host'], port=config['db']['port'],
                                   user=config['db']['user'], passwd=config['db']['pass'], db=config['db']['db'])
        else:
            return None

    def get_by_date(self, date):
        conn = self.__conn()
        df = pd.read_sql('SELECT * FROM stock_data WHERE `date` = \'%s\'' % date, conn)
        conn.close()
        return df

    def get_by_code(self, code):
        conn = self.__conn()
        df = pd.read_sql('SELECT * FROM stock_data WHERE `code` = %d' % code, conn)
        conn.close()
        return df

    def get_last_date_info(self, date):
        conn = self.__conn()
        date = datetime.strptime(date, '%Y-%m-%d') - timedelta(days=1)
        df = pd.read_sql('SELECT * FROM stock_data WHERE `date` = \'%s\'' % date, conn)
        while df.empty:
            date = date - timedelta(days=1)
            df = pd.read_sql('SELECT * FROM stock_data WHERE `date` = \'%s\'' % date, conn)
        return df
