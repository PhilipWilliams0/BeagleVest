import duckdb
from config import DB_PATH

def inspect_data():
    with duckdb.connect(DB_PATH) as conn:
        df = conn.execute("SELECT * FROM market_data ORDER BY date DESC LIMIT 10").fetchdf()
        print(df)

if __name__ == "__main__":
    inspect_data()
