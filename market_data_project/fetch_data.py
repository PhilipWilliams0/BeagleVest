import requests
import pandas as pd
from config import TIINGO_API_KEY
from datetime import datetime

BASE_URL = "https://api.tiingo.com/tiingo/daily/{}/prices"

def fetch_tiingo_data(ticker, start_date, end_date=None):
    end_date = end_date or datetime.today().strftime("%Y-%m-%d")
    url = BASE_URL.format(ticker)
    headers = {"Content-Type": "application/json"}
    params = {
        "startDate": start_date,
        "endDate": end_date,
        "token": TIINGO_API_KEY
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return pd.DataFrame(data)
