# QtShare 数据 API 参考文档
V1.0 | 最后修订：2017/6/13

## 简介
鉴于 TuShare 所使用的新浪财经数据源时常不稳定，Quantra 特别封装了 QtShare 数据模块，整合了 TuShare 数据源与网易财经的爬虫，提供较为稳定的数据服务。

## API 说明

#### qtshare.history(code, date\_start, date\_end)
- 作用：获取某股票在某段时间内的历史数据
- 参数：
	- code：股票代码，int 类型
	- date_start：起始日期，datetime 类型
	- date_end：结束日期，datetime 类型
- 返回类型：pandas.DataFrame，包含的列有：`code`, `date`, `open`, `high`, `low`, `close`, `volume`

#### qtshare.today_list()
- 作用：获取最新的实时行情列表
- 返回类型：pandas.DataFrame，包含的列有：`code`, `name`, `rate`, `open`, `high`, `low`, `price`, `yest_close`, `volume`, `turn_over`

#### qtshare.today_ticks(code)
- 作用：获取某股票在最新交易日的分时数据
- 参数：
	- code：股票代码，int 类型
- 返回类型：pandas.DataFrame，包含的列有：`tick`, `price`, `volume`

#### qtshare.today_quotes(code)
- 作用：获取某股票的最新买卖数据
- 参数：
	- code：股票代码，int 类型
- 返回类型：pandas.DataFrame，包含的列有：
- 0：name，股票名字
1：open，今日开盘价
2：pre_close，昨日收盘价
3：price，当前价格
4：high，今日最高价
5：low，今日最低价
6：bid，竞买价，即“买一”报价
7：ask，竞卖价，即“卖一”报价
8：volume，成交量 maybe you need do volume/100
9：amount，成交金额（元 CNY）
10：b1_v，委买一（笔数 bid volume）
11：b1_p，委买一（价格 bid price）
......
20：a1_v，委卖一（笔数 ask volume）
21：a1_p，委卖一（价格 ask price）
......
30：date，日期
31：time，时间

#### qtshare.stock_news(code)
- 作用：获取某股票的最新通告
- 参数：
	- code：股票代码，int 类型
- 返回类型：pandas.DataFrame，包含的列有：`date`, `type`, `title`, `url`
