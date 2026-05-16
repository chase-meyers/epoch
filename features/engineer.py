import pandas as pd
from config import ROLLING_WINDOW, MOMENTUM_WINDOW

def engineer_features(data):
    df = pd.DataFrame()
    df['Close_pct_change'] = data['Close'].pct_change(periods=1)
    df['rolling_std'] = df['Close_pct_change'].rolling(window=ROLLING_WINDOW).std()
    df['momentum'] = data['Close'].pct_change(periods=MOMENTUM_WINDOW)
    return df.dropna()