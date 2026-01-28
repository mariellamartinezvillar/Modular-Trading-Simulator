import yfinance as yf
import pandas as pd

def fetch_data(ticker: str, start_date: str, end_date: str):
    """
    Download historical closing price data.
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    except Exception:
        raise ValueError(f"Error downloading data for ticker '{ticker}'.")

    if data.empty:
        raise ValueError(f"No data returned for ticker '{ticker}'.\nPlease check the symbol."
                         "\nTip: Use official Yahoo Finance tickers (e.g. TSLA, AAPL, MSFT)")
    
    
    if 'Close' not in data.columns:
        raise ValueError(f"Downloaded data does not contain closing prices.")
        
    data = data[['Close']].dropna()

    if len(data) < 60:
        raise ValueError("Insufficient historical data to compute moving averages."
                         "\nPlease choose a longer data range.")
    
    # Flatten columns
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    return data