import duckdb
import pandas as pd
from config import DB_PATH

def init_db():
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
                volume BIGINT,
                PRIMARY KEY (ticker, date)
            )
        """)

def insert_data(ticker, df: pd.DataFrame):
    df['ticker'] = ticker
    df = df.rename(columns={"adjClose": "adj_close"})
    cols = ['ticker', 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']
    df = df[cols]
    
    with duckdb.connect(DB_PATH) as conn:
        conn.register("temp_df", df)
        conn.execute("""
            INSERT OR REPLACE INTO market_data
            SELECT * FROM temp_df
        """)

def get_last_date(ticker):
    with duckdb.connect(DB_PATH) as conn:
        result = conn.execute("""
            SELECT MAX(date) FROM market_data WHERE ticker = ?
        """, [ticker]).fetchone()
        return result[0]
