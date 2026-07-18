import sqlite3
from pathlib import Path
#Prevents the error of folder not found by creating a new folder if not exist
Path("DATA").mkdir(exist_ok=True)
file_path = Path("DATA/project_data.db")
#creation of database
def get_connection():
    #error handling
    try:
       #connection to the database path
       conn=sqlite3.connect(file_path)
       return(conn)
    except sqlite3.Error():
       return None

