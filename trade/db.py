from functools import lru_cache

import akshare as ak
import duckdb
import numpy as np

from helper import query_timer
from trade import STOCK_HOLDINGS

from trade import df_fake

# 1. 内存数据库创建
con = duckdb.connect(':memory:')

# 2. 自动类型推断建表
con.execute("CREATE TABLE tick_data AS SELECT * FROM df_fake")

@query_timer
def run_query(sql):
    return con.execute(sql).fetchdf()

# 3. 复杂查询示例 (毫秒级响应)
result = run_query("""
    SELECT 
        symbol,
        time_bucket(INTERVAL '5 minutes', timestamp) AS window_start,
        avg(price) AS avg_price,
        sum(volume) AS total_volume
    FROM tick_data
    GROUP BY 1,2
    ORDER BY 2 DESC
    LIMIT 10
""")

# 4. 输出优化（自动对齐）
print(result.to_string(index=False, justify='center'))


# 1. 数据获取（使用akshare封装接口）
def get_data(stock_code="002432"):
    # 实时数据
    real_data = ak.stock_zh_a_spot_em()

    # 历史数据（示例获取日线）
    hist_data = ak.stock_zh_a_hist(symbol=stock_code, period="daily")
    return real_data, hist_data

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
