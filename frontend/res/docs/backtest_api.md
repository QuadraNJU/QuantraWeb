# Quantra 回测 API 参考文档
V1.1 | 最后修订：2017/6/12

## 回测原理
每次回测运行时，回测系统建立一个虚拟账户（初始资金为 100,000,000 元）供策略使用。每个调仓周期收盘时，回测系统将会调用策略，策略此时可调用回测系统提供的 API 获取数据或进行交易操作。

## 策略模板
    # coding=utf-8
    import pandas as pd
    import numpy as np
    import stock.data.qtshare as qts
    
    # 可在此处编写策略初始化相关逻辑
    
    def handle(account):
        # 在此处编写每个持有期的处理逻辑
        pass

## API 说明

### 账户信息 API
此部分 API 用于获取虚拟账户的基本信息。

#### account.params
- 作用：获取当前策略的参数列表
- 类型：dict(str, str)
- 提示：参数为 str 类型，请务必注意参数的类型转换

#### account.cash
- 作用：获取当前账户的可用资金（现金）
- 类型：float

#### account.portfolio
- 作用：获取上一周期结束后的总资金（包含现金和持有股票的价值）
- 类型：float

#### account.sec_pos
- 作用：获取当前持仓的股票列表
- 类型：dict(int, int)，key 为股票代码，value 为持有数量

### 高层数据 API
此部分 API 对部分股票数据进行封装，方便策略调用。

#### account.price
- 作用：获取当天所有股票的交易价格
- 类型：dict(int, int)，key 为股票代码，value 为交易价格

#### account.get_stocks()
- 作用：获取当天可交易的所有股票列表
- 返回类型：list(int)

#### account.get_history(attr, days)
- 作用：获取当天所有股票在一段时间内的历史数据
- 参数：
	- attr：数据类型，可选择 `'open'`, `'high'`, `'low'`, `'close'`, `'adjclose'`, `'volume'`
	- days：获取的天数，不超过 90 天
- 返回类型：dict(int, list(float))，key 为股票代码，value 为该股票的历史数据，由近至远排序

### 交易 API
此 API 可对股票发起交易。

#### account.trade(stock, target)
- 作用：对某个股票发起买入或卖出交易
- 参数：
	- stock：股票代码，int 类型
	- target：目标持有量，即交易后该股票的持有股数
- 返回类型：None
- 注意：买入交易时，若账户中的现金不足，交易将被拒绝

### 底层数据 API
此部分 API 提供对底层股票数据的直接访问，供高级用户使用。

#### account.universe_data
- 作用：获取所选股票池内所有股票在所有日期上的数据
- 类型：pandas.DataFrame

#### account.today_data
- 作用：获取所选股票池内所有股票在当前日期上的数据
- 类型：pandas.DataFrame
