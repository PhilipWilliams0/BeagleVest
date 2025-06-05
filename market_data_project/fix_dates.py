import duckdb
import os
from dotenv import load_dotenv

# Load DB path
load_dotenv()
DB_PATH = os.getenv("DB_PATH", "market_data.duckdb")

# Run update query
with duckdb.connect(DB_PATH) as conn:
    conn.execute("UPDATE market_data SET date = CAST(date AS DATE)")
    print("✅ All datetime values in 'date' column converted to DATE.")
