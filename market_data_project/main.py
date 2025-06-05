import os
import duckdb
import pandas as pd
from tiingo import TiingoClient
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DB_PATH = os.getenv("DB_PATH", "market_data.duckdb")
TIINGO_API_KEY = os.getenv("TIINGO_API_KEY")

# Configure Tiingo client
config = {
    'session': True,
    'api_key': TIINGO_API_KEY
}
tc = TiingoClient(config)

# Load tickers from CSV
def load_tickers(file_path="tickers.csv"):
    return pd.read_csv(file_path)

# Get the last date a ticker has in the database
def get_last_date(ticker):
    with duckdb.connect(DB_PATH) as conn:
        result = conn.execute(
            "SELECT MAX(date) FROM market_data WHERE ticker = ?",
            [ticker]
        ).fetchone()[0]
    return result or datetime(2000, 1, 1).date()

# Create table if not exists
def ensure_table():
    with duckdb.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS market_data (
                ticker TEXT,
                date DATE,
                open DOUBLE,
                high DOUBLE,
                low DOUBLE,
                close DOUBLE,
                adj_close DOUBLE,
                volume BIGINT
            )
        """)

# Insert cleaned data into DB
def insert_data(df: pd.DataFrame):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df["open"] = pd.to_numeric(df["open"], errors="coerce")
    df["high"] = pd.to_numeric(df["high"], errors="coerce")
    df["low"] = pd.to_numeric(df["low"], errors="coerce")
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df["adj_close"] = pd.to_numeric(df["adj_close"], errors="coerce")
    df["volume"] = pd.to_numeric(df["volume"], downcast="integer", errors="coerce")
    df.dropna(subset=["ticker", "date", "open", "high", "low", "close", "adj_close", "volume"], inplace=True)

    if df.empty:
        print("  ⚠️ No valid rows to insert.")
        return

    with duckdb.connect(DB_PATH) as conn:
        conn.register("df", df)
        conn.execute("""
            INSERT INTO market_data (ticker, date, open, high, low, close, adj_close, volume)
            SELECT ticker, date, open, high, low, close, adj_close, volume FROM df
        """)
    print(f"  ✅ Inserted {len(df)} rows.")

# Main logic
def main():
    ensure_table()
    tickers = load_tickers()

    for _, row in tickers.iterrows():
        ticker = row["ticker"]
        company = row["company"]

        print(f"\nProcessing {ticker}...")
        start_date = get_last_date(ticker) + timedelta(days=1)
        print(f"  ⏳ Fetching data starting from {start_date}...")

        try:
            price_data = tc.get_dataframe(ticker, startDate=start_date.strftime("%Y-%m-%d"))
            if price_data.empty:
                print(f"  ⚠️ No new data for {ticker}.")
                continue

            price_data.reset_index(inplace=True)
            price_data = price_data.rename(columns={
                'adjClose': 'adj_close',
                'close': 'close',
                'open': 'open',
                'high': 'high',
                'low': 'low',
                'volume': 'volume',
                'date': 'date'
            })
            price_data["date"] = pd.to_datetime(price_data["date"]).dt.date
            price_data["ticker"] = ticker
            insert_data(price_data)

        except Exception as e:
            print(f"  ❌ Error fetching {ticker}: {e}")
            print(f"  ⚠️ No new data for {ticker}.")

if __name__ == "__main__":
    main()
