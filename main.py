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

# Create the "Completed Models" db table if it doesn't exist
c.execute("""
    CREATE TABLE IF NOT EXISTS completed_models (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT NOT NULL,
        completed BOOLEAN DEFAULT 0,
        completed_date TEXT DEFAULT NULL 
    )""")

update_query = "UPDATE completed_models SET completed = 1, completed_date = datetime('now', 'localtime') WHERE model = ?" 
insert_query = "INSERT INTO completed_models (model) VALUES (?)"

#main loop
def run():

    #get available models
    c.execute("SELECT model, completed FROM completed_models")
    models = c.fetchall()
    '''
    #uncomment to load models into completed_models table
    completed_models_load = []
    for model in models:
        insert_tuple = (model,)
        completed_models_load.append(insert_tuple)

    c.executemany(insert_query, completed_models_load)
    conn.commit()
    '''

    print("Available Models:")
    print("-" * 30)
    for idx, (model_name, completed) in enumerate(models, start=1):
        if completed:
            completed_string = "\033[32mCompleted\033[0m"
        else:
            completed_string = "\033[31mNot Completed\033[0m"
        print(f"{idx}. {model_name} ----- {completed_string}")

    #user selects model
    selected_model = None
    while selected_model is None:
        try:
            choice = int(input(f"Select a model (1-{len(models)}): "))
            if 1 <= choice <= len(models):
                selected_model = models[choice - 1][0]
            else:
                print("Invalid number. Try again.")
        except ValueError:
            print("Please enter a number.")

    print(f"You selected: {selected_model}")
    time.sleep(2)
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
    time.sleep(2)
    #get options for selected model
    c.execute("SELECT model_year, model_code, option_code, option_name, option_category, invoice_price, msrp_price FROM model_options WHERE model = ?", (selected_model,))
    rows = c.fetchall()

    #get all paints for selected model
    c.execute("SELECT option_code FROM model_options WHERE model = ? AND option_category = ?", (selected_model, "EXT"))
    paints = [row[0] for row in c.fetchall()]

    #get all interiors for selected model
    c.execute("SELECT option_code FROM model_options WHERE model = ? AND option_category = ?", (selected_model, "INT"))
    interiors = [row[0] for row in c.fetchall()]
    time.sleep(2)

    #start interacting with PCS Tables
    pcslib.focus_pcs()
    #order of select_model(model_year, model_code)
    pcslib.select_model(rows[0][1], str(rows[0][0]))
    time.sleep(2)
    #loop through all options
    for row in rows:
        #order of select_option(option, name, category, invoice, msrp)
        pcslib.select_option(row[2], row[3], row[4], row[5], row[6])
        pcslib.option_back_reset()
    #add all paints and interiors to EXT1 and INT1 (currently)
    pcslib.add_paints(paints)
    pcslib.add_interiors(interiors)
    #back out of options screen
    pcslib.back()
    #reverse tab back to model search box
    pcslib.back_reset()
    c.execute(update_query, (selected_model,))
    conn.commit()
    conn.close()



if __name__ == "__main__":
    run()