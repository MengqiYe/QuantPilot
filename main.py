import numpy as np
import pandas as pd
from tabulate import tabulate

from trade.db import get_data, simple_ma_strategy, con, run_query, get_stock_data
from trade.df_calc import calculate_technical
from trade.df_plot import plot_analysis


def main():
    # 执行分析
    symbol = "002432"
    df = get_stock_data(symbol)
    df = calculate_technical(df)

    # 打印最新数据
    print("最新技术指标：")
    print(df[['close', 'MA5', 'MA20', 'RSI14', 'MACD']].tail(3))

    # 生成交易信号
    df['Signal_MA'] = pd.Series(0, index=df.index)
    df['Signal_MA'] = np.where(df['MA5'] > df['MA20'], 1, -1)
    df['Position_MA'] = df['Signal_MA'].diff()

    print("\n近期交易信号：")
    print(df[['close', 'MA5', 'MA20', 'Position_MA']].tail(5))

    # 可视化
    plot_analysis(df[-120:])  # 显示最近120个交易日

if __name__ == "__main__":
    main()