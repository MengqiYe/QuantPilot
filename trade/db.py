from functools import lru_cache

import akshare as ak
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from helper import query_timer
from trade import STOCK_HOLDINGS

# 1. 内存数据库创建
con = duckdb.connect(':memory:')



@query_timer
def run_query(sql):
    return con.execute(sql).fetchdf()


# 1. 数据获取（使用akshare封装接口）
def get_data(stock_code="002432"):
    # 实时数据
    real_data = ak.stock_zh_a_spot_em()

    # 历史数据（示例获取日线）
    hist_data = ak.stock_zh_a_hist(symbol=stock_code, period="daily")
    return real_data, hist_data


def get_stock_data(symbol="002432"):
    # 自动添加交易所后缀
    symbol_with_suffix = f"{symbol}.SZ" if symbol.startswith('00') else f"{symbol}.SH"

    df = ak.stock_zh_a_hist(
        symbol=symbol,
        period="daily",
        start_date="20190101",
        end_date=datetime.now().strftime("%Y%m%d"),
        adjust="qfq"  # 前复权
    )

    # 数据清洗
    df.rename(columns={
        '日期': 'date',
        '开盘': 'open',
        '最高': 'high',
        '最低': 'low',
        '收盘': 'close',
        '成交量': 'volume'
    }, inplace=True)

    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df.dropna()

# 2. 策略实现（示例：简单均线策略）
def simple_ma_strategy(data, short_window=5, long_window=20):
    data['short_ma'] = data['收盘'].rolling(short_window).mean()
    data['long_ma'] = data['收盘'].rolling(long_window).mean()
    data['signal'] = np.where(data['short_ma'] > data['long_ma'], 1, -1)
    return data

# 使用缓存
@lru_cache(maxsize=128)
def cached_data(stock_code):
    return ak.stock_zh_a_hist(stock_code)

# 并行处理
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor() as executor:
    results = executor.map(get_data, STOCK_HOLDINGS)
