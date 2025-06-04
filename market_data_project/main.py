from fetch_data import fetch_tiingo_data
from database import init_db, insert_data, get_last_date
from datetime import timedelta
import pandas as pd

def load_tickers(file_path="tickers.csv"):
    return pd.read_csv(file_path)

def main():
    init_db()
    ticker_df = load_tickers()

    for _, row in ticker_df.iterrows():
        ticker = row['ticker']
        company = row['company']
        print(f"Processing {ticker}...")

        last_date = get_last_date(ticker)
        if last_date:
            start_date = (pd.to_datetime(last_date) + timedelta(days=1)).strftime("%Y-%m-%d")
        else:
            start_date = "2000-01-01"

        df = fetch_tiingo_data(ticker, start_date=start_date)
        if not df.empty:
            insert_data(ticker, df)
            print(f"{ticker} updated with {len(df)} rows.")
        else:
            print(f"No new data for {ticker}.")
