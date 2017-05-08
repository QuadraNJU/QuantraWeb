import json
import pandas as pd

import MySQLdb


class StockData:
    def __conn(self):
        config = json.load(open('../../global_config.json'))
        if config['db']:
            return MySQLdb.connect(host=config['db']['host'], port=config['db']['port'],
                                   user=config['db']['user'], passwd=config['db']['pass'], db=config['db']['db'])
        else:
            return None

    def get_by_date(self, date):
        conn = self.__conn()
        df = pd.read_sql('SELECT * FROM stock_info WHERE `date` = \'%s\'' % date)
        conn.close()
        return df

    def get_by_code(self, code):
        conn = self.__conn()
        df = pd.read_sql('SELECT * FROM stock_info WHERE `code` = %d' % code)
        conn.close()
        return df
