import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def calculate_bollinger_bands(df, window=20, num_std_dev=2):
    df['Middle_Band'] = df['close'].rolling(window=window).mean()

    df['Upper_Band'] = df['Middle_Band'] + (df['close'].rolling(window=window).std() * num_std_dev)
    df['Lower_Band'] = df['Middle_Band'] - (df['close'].rolling(window=window).std() * num_std_dev)

    return df

def generate_signals(df):
    df['Signal'] = 0
    df.loc[df['close'] < df['Lower_Band'], 'Signal'] = 1   
    df.loc[df['close'] > df['Upper_Band'], 'Signal'] = -1 

    df['Position'] = df['Signal'].diff()
    
    return df

def calculate_returns(df):
    df['Market_Returns'] = df['close'].pct_change()
    df['Strategy_Returns'] = df['Market_Returns'] * df['Signal'].shift(1)

    df['Cumulative_Market_Returns'] = (1 + df['Market_Returns']).cumprod()
    df['Cumulative_Strategy_Returns'] = (1 + df['Strategy_Returns']).cumprod()

    return df