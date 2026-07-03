import pandas as pd
import sqlite3
from app_model.db import get_connection
def get_all_cyber_incidents():
    conn = get_connection()
    if conn == None :
        print("Failed connection with database")
    else :
       data=[]
       try:
          sql = ("SELECT * FROM cyber_incidents")
          data = pd.read_sql(sql, conn)
       except sqlite3.Error:
           print("Error could not read the database")
       finally:
          conn.close()
       return data