import matplotlib.pyplot as plt

# 可视化
# RSI看冷热，布林测弹性
# MACD判趋势，三者要配合
# 超买莫追高，超跌别恐慌
# 金叉可试水，死叉先避险
def plot_analysis(df):
    plt.figure(figsize=(16, 12))

    # 价格与均线
    plt.subplot(4, 1, 1)
    plt.plot(df['close'], label='Close')
    plt.plot(df['MA5'], label='MA5')
    plt.plot(df['MA20'], label='MA20')
    plt.plot(df['MA60'], label='MA60')
    plt.title('Price & Moving Averages')
    plt.legend()

    # RSI
    plt.subplot(4, 1, 2)
    plt.plot(df['RSI14'], label='RSI14', color='purple')
    plt.axhline(70, linestyle='--', color='red')
    plt.axhline(30, linestyle='--', color='green')
    plt.title('RSI Indicator')

    # 布林带
    plt.subplot(4, 1, 3)
    plt.plot(df['close'], label='Close')
    plt.plot(df['BB_upper'], label='Upper Band', linestyle='--')
    plt.plot(df['BB_middle'], label='Middle Band')
    plt.plot(df['BB_lower'], label='Lower Band', linestyle='--')
    plt.fill_between(df.index, df['BB_upper'], df['BB_lower'], alpha=0.1)
    plt.title('Bollinger Bands')

    # MACD
    plt.subplot(4, 1, 4)
    plt.bar(df.index, df['Hist'], label='Histogram', color='gray')
    plt.plot(df['MACD'], label='MACD', color='blue')
    plt.plot(df['Signal'], label='Signal', color='orange')
    plt.title('MACD')

    plt.tight_layout()
    plt.show()