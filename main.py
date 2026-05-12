import os
import sqlite3
import time
from dotenv import load_dotenv
import pcslib

# Load environment variables
load_dotenv()

DB_URL = os.getenv("DB_URL")

# 3 digit codes for all PCS Divisions
divisions = [
    "ADG", "AJP", "ADO", "ASD", "AUD", "AVW", "CHR", "DGT", "DOD", "JEP",
    "PLY", "FEI", "FOR", "FTK", "LNC", "MER", "BUI", "CAD", "CHE", "CHT",
    "GMC", "HAX", "HD", "HNP", "HYA", "HYU", "IPX", "LEX", "MBA", "MBO",
    "NAX", "NPX", "PSS", "PXC", "PXP", "SUA", "SUB", "SVW", "TOY", "TYP",
    "USC", "USP"
]


# Connect to the database
conn = sqlite3.connect(DB_URL)
c = conn.cursor()


#main loop
def run():

    #get available models
    c.execute("SELECT DISTINCT model FROM model_options ORDER BY model")
    models = [row[0] for row in c.fetchall()]
    print("Available Models:")
    print("-" * 30)
    for idx, model in enumerate(models, start=1):
        print(f"{idx}. {model}")

    #user selects model
    selected_model = None
    while selected_model is None:
        try:
            choice = int(input(f"Select a model (1-{len(models)}): "))
            if 1 <= choice <= len(models):
                selected_model = models[choice - 1]
            else:
                print("Invalid number. Try again.")
        except ValueError:
            print("Please enter a number.")

    print(f"You selected: {selected_model}")
    time.sleep(5)
    print("Available Divisions:")
    print("-" * 30)
    for idx, div in enumerate(divisions, start=1):
        print(f"{idx}. {div}")

    #user selects Division (used in PCS later)
    selected_division = None
    while selected_division is None:
        try:
            choice = int(input(f"Select a division (1-{len(divisions)}): "))
            if 1 <= choice <= len(divisions):
                selected_division = divisions[choice - 1]
            else:
                print("Invalid number. Try again.")
        except ValueError:
            print("Please enter a number.")

    print(f"You selected division: {selected_division}")
    time.sleep(5)
    c.execute("SELECT model_year, model_code, option_code, option_name, option_category, invoice_price, msrp_price FROM model_options WHERE model = ?", (selected_model,))
    rows = c.fetchall()
    pcslib.focus_pcs()
    pcslib.select_model(rows[0][1], str(rows[0][0]))
    time.sleep(2)
    for row in rows:
        pcslib.select_option(row[2], row[3], row[4], row[5], row[6])
        pcslib.option_back_reset()
    pcslib.back()
    pcslib.back_reset()
    conn.close()



if __name__ == "__main__":
    run()