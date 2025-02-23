import pandas as pd
from tabulate import tabulate

from trade.db import get_data, simple_ma_strategy






# 3. 执行流程
if __name__ == "__main__":
    # 获取数据
    real_time, historical = get_data()

    # 运行策略
    strategy_data = simple_ma_strategy(historical)
    display_df = strategy_data[['日期', '收盘', 'short_ma', 'long_ma', 'signal']].tail()

    # 输出交易信号
    # 打印居中对齐表格
    # 设置显示格式
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.width', 10)
    display_df = display_df.astype(str).apply(lambda x: x.str.center(10))

    print(display_df.to_string(index=False))

    # 打印居中对齐表格
    print(tabulate(display_df,
                   headers='keys',
                   tablefmt='psql',
                   stralign='left',
                   showindex=False))

