#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# imports all necessaries libraries
import numpy as np
import pandas as pd

# defines useful functions
def compute_technical_indicators(df):
    df = df.copy()
    df['return'] = df['Close'].pct_change()
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['volatility_20'] = df['return'].rolling(window=20).std() * np.sqrt(252)

    # RSI simple implementation
    delta = df['Close'].diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    roll_up = up.rolling(14).mean()
    roll_down = down.rolling(14).mean()
    rs = roll_up / (roll_down + 1e-6)
    df['RSI_14'] = 100 - (100 / (1 + rs))
    return df.dropna()

def prepare_lag_features(df, n_lags=5):
    df = df.copy()
    for lag in range(1, n_lags+1):
        df[f'lag_close_{lag}'] = df['Close'].shift(lag)
        df['target_next_close'] = df['Close'].shift(-1)
    return df.dropna()

