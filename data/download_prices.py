"""
Downloads historical daily closing prices for a list of selected tickers from Yahoo Finance
between 2015-01-01 and 2024-01-01, removes stocks with missing data, and saves the cleaned
data as a CSV file at 'data/price.csv'.
"""

import yfinance as yf
import pandas as pd

tickers = [
    "AAPL", "MSFT", "GOOG", "AMZN", "META", "NVDA", "TSLA", "NFLX", "ADBE", "CRM",
    "ORCL", "INTC", "AMD", "CSCO", "QCOM", "AVGO", "TXN", "IBM", "PYPL", "SHOP"
]
data = yf.download(tickers, start="2015-01-01", end="2024-01-01")["Close"]
data.dropna(axis=1, inplace=True)  # Drop stocks with missing data
data.to_csv("data/price.csv")