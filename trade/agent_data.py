import pandas as pd
import numpy as np

# 生成测试数据
df_fake = pd.DataFrame({
    'timestamp': pd.date_range('2023-01-01', periods=1_000_000, freq='s'),
    'symbol': np.random.choice(['AAPL', 'MSFT', 'GOOG'], 1_000_000),
    'price': np.random.normal(100, 5, 1_000_000),
    'volume': np.random.randint(1000, 10000, 1_000_000)
})
