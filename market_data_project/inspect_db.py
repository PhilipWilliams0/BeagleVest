import duckdb
import os
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DB_PATH", "market_data.duckdb")

with duckdb.connect(DB_PATH) as conn:
    result = conn.execute("""
        SELECT ticker, COUNT(*) as rows, MIN(date) as start_date, MAX(date) as end_date
        FROM market_data
        GROUP BY ticker
        ORDER BY ticker
    """).fetchdf()

print("\n📊 Current ticker coverage in database:\n")
print(result.to_string(index=False))
