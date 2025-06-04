from export_to_excel import export_ticker_to_excel
from main import load_tickers

def main():
    ticker_df = load_tickers()
    print(ticker_df)  # 👈 Confirm tickers loaded

    for _, row in ticker_df.iterrows():
        print(f"Exporting {row['ticker']} - {row['company']}")
        export_ticker_to_excel(row["ticker"], row["company"])

if __name__ == "__main__":
    main()
