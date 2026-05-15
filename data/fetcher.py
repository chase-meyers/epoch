import sys
from pathlib import Path

# Add parent directory to sys.path to allow imports from config.py
sys.path.append(str(Path(__file__).parent.parent))

import yfinance as yf
from config import START_DATE, DEFAULT_TICKER
from datetime import date, timedelta
import pandas as pd
import logging
logging.getLogger('yfinance').setLevel(logging.CRITICAL)

def fetch_data(ticker):
    # Placeholder for data fetching logic
    print("Fetching data...")

    tick = yf.Ticker(ticker)
    today = date.today()

    # Last market close is typically yesterday's date, so we fetch data up to yesterday
    yesterday = today - timedelta(days=1)

    try:
        data = tick.history(start=START_DATE, end=yesterday)
        if data.empty:
            raise ValueError(f"No data found for {ticker}")
        
    except Exception:
        print(f"Error fetching data for ticker {ticker}")
        print(f"Using default ticker {DEFAULT_TICKER} instead.")
        try:
            tick = yf.Ticker(DEFAULT_TICKER)
            data = tick.history(start=START_DATE, end=yesterday)

        except Exception as e:
            print(f"Error: DEFAULT_TICKER also failed: {e}")
            return None

    if data.empty:
        print(f"Error: No data found")
        return None
    
    return data

