import pandas as pd
import sqlite3
import streamlit as st
from app_model.db import get_connection
#Querying SQLite to a Dataframe
@st.cache_data(ttl=600)
#fetching all the it tickets
def get_all_it_tickets():
    conn=get_connection()
    if conn == None :
        print("Failed connection with database")
    else :
        #returns empty list if there is an error
        data=[]
        try:
           sql=("SELECT*FROM it_tickets")
           data=pd.read_sql(sql,conn)
        except sqlite3.Error :
            print("Could not read the database")
        finally:
            conn.close
        return(data)