import os
import sqlite3
import time
from dotenv import load_dotenv
import pcslib

# Load environment variables
load_dotenv()

DB_URL = os.getenv("DB_URL")


# Connect to the database
conn = sqlite3.connect(DB_URL)
c = conn.cursor()

#create table if it doesn't exist
c.execute("""
        CREATE TABLE IF NOT EXISTS model_options(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_year INTEGER NOT NULL,
            division TEXT NOT NULL,
            model TEXT NOT NULL,
            model_code TEXT NOT NULL,
            option_code TEXT NOT NULL,
            option_name TEXT DEFAULT NULL,
            option_category TEXT DEFAULT NULL,
            invoice_price REAL NOT NULL,
            msrp_price REAL NOT NULL,
            scrape_date TEXT DEFAULT (datetime('now', 'localtime'))
        )""")

#SQL query used later to insert using executemany()
sql = """INSERT INTO model_options (model_year, division, model, model_code, option_code, option_name, option_category, invoice_price, msrp_price)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
#end helper functions

#main loop
def run():
    #insert data into database
    c.executemany(sql, data)

    conn.commit()
    conn.close()



if __name__ == "__main__":
    run()