import os
import duckdb
import pandas as pd
import xlsxwriter
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "market_data.duckdb")


def export_ticker_to_excel(ticker, company, export_dir="exports"):
    os.makedirs(export_dir, exist_ok=True)

    with duckdb.connect(DB_PATH) as conn:
        df = conn.execute("""
            SELECT * FROM market_data
            WHERE ticker = ?
            ORDER BY date
        """, [ticker]).df()

    if df.empty:
        print(f"No data to export for {ticker}")
        return

    # Ensure 'date' column is date only
    df["date"] = pd.to_datetime(df["date"]).dt.date

    file_path = os.path.join(export_dir, f"{ticker}.xlsx")
    with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Daily")

        workbook = writer.book
        worksheet = writer.sheets["Daily"]

        # Set column format for date
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
        worksheet.set_column("B:B", 15, date_format)  # 'date' is column B

        chart = workbook.add_chart({"type": "line"})
        chart.add_series({
            "name":       f"{ticker}",
            "categories": ["Daily", 1, 1, len(df), 1],  # date column (B)
            "values":     ["Daily", 1, 6, len(df), 6],  # adj_close column (G)
        })
        chart.set_title({"name": f"{company} ({ticker}) - Adj Close"})
        chart.set_x_axis({"name": "Date"})
        chart.set_y_axis({"name": "Price"})

        worksheet.insert_chart("J2", chart)

    print(f"✅ Exported (xlsxwriter): {file_path}")