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

    def get_index(self):
        conn = self.__conn()
        df = pd.read_sql('SELECT * FROM stock_index', conn, index_col='code')
        conn.close()
        return df

    def get_by_date(self, date):
        conn = self.__conn()
        df = pd.read_sql('SELECT * FROM stock_data WHERE `date` = \'%s\'' % date, conn, index_col='code')
        conn.close()
        return df

    def get_by_code(self, code):
        conn = self.__conn()
        df = pd.read_sql('SELECT * FROM stock_data WHERE `code` = %d' % code, conn)
        conn.close()
        return df

    def get_yesterday_info(self, date):
        conn = self.__conn()
        for i in range(1, 4):
            date = datetime.strptime(date, '%Y-%m-%d') - timedelta(days=i)
            df = pd.read_sql('SELECT * FROM stock_data WHERE `date` = \'%s\'' % date, conn, index_col='code')
            if not df.empty:
                conn.close()
                return df
        conn.close()
        return pd.DataFrame()
