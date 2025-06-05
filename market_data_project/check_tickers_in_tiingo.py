import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("TIINGO_API_KEY")
BASE_URL = "https://api.tiingo.com/tiingo/daily"

def check_ticker_exists(ticker):
    url = f"{BASE_URL}/{ticker}"
    response = requests.get(url, params={"token": API_KEY})
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        print(f"⚠️ Error checking {ticker}: {response.status_code}")
        return None

def main():
    tickers_df = pd.read_csv("tickers.csv")  # Must contain columns: ticker, company

    print("\n📡 Checking ticker availability on Tiingo:\n")
    results = []

    for _, row in tickers_df.iterrows():
        ticker = row["ticker"]
        company = row["company"]
        exists = check_ticker_exists(ticker)

        status = "✅ Exists" if exists else "❌ Not Found" if exists is False else "⚠️ Error"
        print(f"{ticker:5} - {company:35} => {status}")
        results.append({"ticker": ticker, "company": company, "status": status})

    # Optional: Save results to a CSV
    pd.DataFrame(results).to_csv("tiingo_ticker_check_results.csv", index=False)
    print("\n✅ Results saved to: tiingo_ticker_check_results.csv")

if __name__ == "__main__":
    main()
