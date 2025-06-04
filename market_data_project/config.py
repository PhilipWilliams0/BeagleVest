import os
from dotenv import load_dotenv

load_dotenv()

TIINGO_API_KEY = os.getenv("TIINGO_API_KEY")
DB_PATH = "market_data.db"
