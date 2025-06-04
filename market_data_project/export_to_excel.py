import duckdb
import pandas as pd
import os
from config import DB_PATH

def export_ticker_to_excel(ticker, company_name, output_dir="exports"):
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Fetch data
    with duckdb.connect(DB_PATH) as conn:
        df = conn.execute("""
            SELECT date, open, high, low, close, adj_close, volume
            FROM market_data
            WHERE ticker = ?
            ORDER BY date
        """, [ticker]).fetchdf()

    if df.empty:
        print(f"No data to export for {ticker}")
        return

    df = df.dropna(subset=["date", "adj_close"])
    df["date"] = pd.to_datetime(df["date"]).dt.date

    file_path = os.path.join(output_dir, f"{ticker}.xlsx")

    # Step 2: Write with xlsxwriter
    with pd.ExcelWriter(file_path, engine='xlsxwriter', date_format='yyyy-mm-dd') as writer:
        df.to_excel(writer, sheet_name=ticker, index=False)
        workbook  = writer.book
        worksheet = writer.sheets[ticker]

        # Step 3: Write metadata
        worksheet.write("I1", "Ticker")
        worksheet.write("I2", ticker)
        worksheet.write("J1", "Company Name")
        worksheet.write("J2", company_name)

        # Step 4: Create chart
        chart = workbook.add_chart({'type': 'line'})

        row_count = len(df)

        chart.add_series({
            'name':       'Adj Close',
            'categories': [ticker, 1, 0, row_count, 0],  # A2:A{n+1} (date)
            'values':     [ticker, 1, 5, row_count, 5],  # F2:F{n+1} (adj_close)
        })

        chart.set_title({'name': company_name})
        chart.set_x_axis({'name': 'Date'})
        chart.set_y_axis({'name': 'Adj Close'})
        chart.set_style(10)

        # Step 5: Insert chart
        worksheet.insert_chart('L4', chart)

    print(f"✅ Exported (xlsxwriter): {file_path}")
