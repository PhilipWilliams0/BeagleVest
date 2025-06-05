import duckdb
import pandas as pd
from config import DB_PATH

with duckdb.connect(DB_PATH) as conn:
    df = conn.execute("SELECT * FROM market_data WHERE ticker = 'DUOL' LIMIT 5").fetchdf()

print(df.dtypes)
print(df.head())
