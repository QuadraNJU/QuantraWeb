import json

import MySQLdb
import pandas as pd
from datetime import timedelta, datetime


class StockData:
    def __conn(self):
        config = json.load(open('global_config.json'))
        if config['db']:
            return MySQLdb.connect(host=config['db']['host'], port=config['db']['port'], charset='utf8',
                                   user=config['db']['user'], passwd=config['db']['pass'], db=config['db']['db'])
        else:
            return None

    def get_info(self, target_code=None, target_date=None):
        conn = self.__conn()
        sql = 'SELECT * FROM stock_data'
        if target_code is not None and target_date is None:
            sql = 'SELECT * FROM stock_data WHERE `code` = ' + str(target_code)
        elif target_code is None and target_date is not None:
            sql = 'SELECT * FROM stock_data WHERE `date` = \'{}\''.format(target_date)
        elif target_code is not None and target_date is not None:
            sql = 'SELECT * FROM stock_data WHERE `date` = \'%s\' AND `code` = %d' \
                % (target_date, target_code)
        df = pd.read_sql(sql, conn, index_col='code')
        conn.close()
        return df

    def get_index(self):
        conn = self.__conn()
        df = pd.read_sql('SELECT * FROM stock_index', conn, index_col='code')
        conn.close()
        return df

    def get_by_date(self, date):
        return self.get_info(target_date=date)

    def get_by_code(self, code):
        return self.get_info(target_code=code)

    def get_yesterday_info(self, date):
        return self.get_days_before(date, 1)

    def get_days_before(self, date, n):
        conn = self.__conn()
        for i in range(n, n+4):
            date = date - timedelta(days=i)
            df = pd.read_sql('SELECT * FROM stock_data WHERE `date` = \'%s\'' % date, conn, index_col='code')
            if not df.empty:
                conn.close()
                return df
        conn.close()
        return pd.DataFrame()
