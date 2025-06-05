import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
TIINGO_API_KEY = os.getenv("TIINGO_API_KEY")
HEADERS = {"Content-Type": "application/json"}

def check_data(ticker):
    url = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices"
    params = {"startDate": "2000-01-01", "resampleFreq": "daily", "token": TIINGO_API_KEY}
    resp = requests.get(url, headers=HEADERS, params=params)
    if resp.status_code != 200:
        return f"❌ API error {resp.status_code}"
    data = resp.json()
    return f"{len(data)} records found" if data else "⚠️ No price data returned"

tickers = [
    "AAPL", "MSFT", "ELF", "SMCI", "CELH", "INSP",
    "AXON", "TMDX", "NVCR", "DUOL", "MODG", "RXRX"
]

for ticker in tickers:
    print(f"{ticker:5} -> {check_data(ticker)}")
