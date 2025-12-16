import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm

def resample_ohlc(df, timeframe):
    return df.resample(timeframe).agg({
        "price": "ohlc",
        "qty": "sum"
    }).dropna()

def log_returns(series):
    return np.log(series / series.shift(1)).dropna()

def rolling_volatility(returns, window):
    return returns.rolling(window).std()

def hedge_ratio(y, x):
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    return model.params[1]

def spread(y, x, hedge):
    return y - hedge * x

def zscore(series, window):
    return (series - series.rolling(window).mean()) / series.rolling(window).std()

def rolling_corr(x, y, window):
    return x.rolling(window).corr(y)

def adf_test(series):
    result = adfuller(series.dropna())
    return {
        "adf_stat": result[0],
        "p_value": result[1],
        "stationary": result[1] < 0.05
    }
