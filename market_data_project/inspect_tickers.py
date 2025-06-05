import duckdb
import os
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DB_PATH", "market_data.duckdb")

with duckdb.connect(DB_PATH) as conn:
    df = conn.execute("SELECT DISTINCT ticker FROM market_data ORDER BY ticker").fetchdf()
    print("📊 Tickers in database:\n")
    print(df)
