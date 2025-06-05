from export_to_excel import export_ticker_to_excel
import pandas as pd

def main():
    print("\n📦 Running export_all.py...\n")
    tickers = pd.read_csv("tickers.csv")
    print(tickers)

    for _, row in tickers.iterrows():
        export_ticker_to_excel(row["ticker"], row["company"])

if __name__ == "__main__":
    main()
