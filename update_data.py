from datetime import timedelta, datetime

from stock.data.stock_data import StockData
import stock.data.qtshare as qts


if __name__ == '__main__':
    sd = StockData()
    index = sd.get_index()
    print('Total:', len(index))
    end_date = datetime.now()
    count = 0
    for code, row in index.iterrows():
        try:
            max_date = sd.get_info(code=code, limit=1).iloc[0]['date']
            start_date = max_date + timedelta(days=1)
            df = qts.history(code, start_date, end_date)
            df['adjclose'] = df['close']
            print(df)
            df.to_sql('stock_data', sd.conn, index=False, if_exists='append')
            count += 1
            print('Finished:', code, ', progress:', count, '/', len(index))
        except:
            pass
