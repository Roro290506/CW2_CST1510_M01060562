import streamlit as st
import sqlite3
from app_model.db import get_connection
#get all logs
@st.cache_data(ttl=600)
def get_all_logs():
    conn=get_connection()
    #to check if communication with database has been established
    if conn == None :
        print("Failed connection with database")
    else :
        #declaration of emply logs list
        logs=[]
        #in the event of an error when fetching logs the empty list is returned
        try:
          cur=conn.cursor()
          cur.execute("SELECT * FROM logs")
          logs=cur.fetchall()
        finally:
          conn.close()
        return logs 
  
#inserting log details into the log table
def insert_log(user_id,login_time,logout_time):
    conn=get_connection()
    if conn == None :
        print("Failed connection with database")
    else :
        cur=conn.cursor()
        try:
            #inserting information about a log
            sql=('''INSERT INTO logs(user_id,login_time,logout_time) VALUES(?,?,?)''')
            cur.execute(sql,(user_id,login_time,logout_time))
            conn.commit()
        except sqlite3.Error:
            print("Insertion of log failed")
        finally:
          conn.close()