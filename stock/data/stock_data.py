import json

import pandas as pd
from sqlalchemy import table, create_engine, select, column


class StockData:
    def __init__(self):
        config = json.load(open('global_config.json'))
        if config['db']:
            self.conn = create_engine(
                'mysql://%s:%s@%s:%d/%s?charset=utf8' %
                (config['db']['user'], config['db']['pass'], config['db']['host'],
                 config['db']['port'], config['db']['db'])
            )

    def get_info(self, code=None, date=None, date_start=None):
        if code is None and date is None:
            return pd.DataFrame()
        s = select('*').select_from(table('stock_data')).order_by('date desc, code desc')
        if code is not None:
            s = s.where(column('code') == code)
        if date is not None:
            if date_start is not None:
                s = s.where(column('date') <= date).where(column('date') >= date_start)
            else:
                s = s.where(column('date') == date)
        df = pd.read_sql(s, self.conn, index_col='code')
        return df

    def get_index(self):
        return pd.read_sql('SELECT * FROM stock_index', self.conn, index_col='code')

    def get_date_range(self):
        result = self.conn.execute('SELECT MIN(date), MAX(date) FROM stock_data')
        data = result.fetchone()
        return data[0], data[1]
