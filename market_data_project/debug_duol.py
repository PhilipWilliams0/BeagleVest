import duckdb
import os
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DB_PATH", "market_data.duckdb")

with duckdb.connect(DB_PATH) as conn:
    df = conn.execute("""
        SELECT * FROM market_data
        WHERE ticker = 'DUOL'
        ORDER BY date DESC
        LIMIT 5
    """).fetchdf()

print(df)
