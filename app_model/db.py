import sqlite3
from pathlib import Path
#Prevents the error of folder not found
Path("DATA").mkdir(exist_ok=True)
file_path = Path("DATA/project_data.db")
#creation of database
def get_connection():
    try:
       conn=sqlite3.connect(file_path)
       return(conn)
    except sqlite3.Error():
       return None

    