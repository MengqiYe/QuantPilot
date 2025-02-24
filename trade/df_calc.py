
# 尝试导入TA-Lib，若不可用则使用手动计算
try:
    import talib
    TA_LIB_AVAILABLE = True
except ImportError:
    TA_LIB_AVAILABLE = False
    print("TA-Lib未安装，使用Pandas计算方法")

# 技术指标计算
def calculate_technical(df):
    # 移动平均线
    df['MA5'] = df['close'].rolling(5).mean()
    df['MA20'] = df['close'].rolling(20).mean()
    df['MA60'] = df['close'].rolling(60).mean()

    # RSI
    if TA_LIB_AVAILABLE:
        df['RSI14'] = talib.RSI(df['close'], timeperiod=14)
    else:
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()
        rs = avg_gain / avg_loss
        df['RSI14'] = 100 - (100 / (1 + rs))

    # 布林带
    if TA_LIB_AVAILABLE:
        upper, middle, lower = talib.BBANDS(df['close'], timeperiod=20)
        df['BB_upper'] = upper
        df['BB_middle'] = middle
        df['BB_lower'] = lower
    else:
        df['BB_middle'] = df['close'].rolling(20).mean()
        std = df['close'].rolling(20).std()
        df['BB_upper'] = df['BB_middle'] + 2 * std
        df['BB_lower'] = df['BB_middle'] - 2 * std

    # MACD
    if TA_LIB_AVAILABLE:
        macd, signal, hist = talib.MACD(df['close'],
                                        fastperiod=12,
                                        slowperiod=26,
                                        signalperiod=9)
        df['MACD'] = macd
        df['Signal'] = signal
        df['Hist'] = hist
    else:
        exp12 = df['close'].ewm(span=12, adjust=False).mean()
        exp26 = df['close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp12 - exp26
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['Hist'] = df['MACD'] - df['Signal']

    return df.dropna()
