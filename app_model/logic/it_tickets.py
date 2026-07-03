import pandas as pd
import sqlite3
from app_model.db import get_connection
#Querying SQLite to a Dataframe
def get_all_it_tickets():
    conn=get_connection()
    if conn == None :
        print("Failed connection with database")
    else :
        data=[]
        try:
           sql=("SELECT*FROM it_tickets")
           data=pd.read_sql(sql,conn)
        except sqlite3.Error :
            print("Could not read the database")
        finally:
            conn.close
        return(data)