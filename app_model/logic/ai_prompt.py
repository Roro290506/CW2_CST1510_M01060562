import streamlit as st
import sqlite3
from app_model.db import get_connection
#for fetching data tomake it faster to store the datatha was already cached instead of reload all of the data
@st.cache_data(ttl=600)
def get_all_prompt():
    conn=get_connection()
    #to check if communication with database has been established
    if conn == None :
        print("Failed connection with database")
    else :
        #declaration of emply prompts list
        prompts=[]
        #in the event of an error when fetching prompts the empty list is returned
        try:
          cur=conn.cursor()
          cur.execute("SELECT * FROM ai_prompt")
          prompts=cur.fetchall()
        finally:
          conn.close()
        return prompts
#used to insert ai prompts into the ai prompt table
def insert_prompt(user_id,prompt,response,response_time):
    #establishing connection
    conn=get_connection()
    if conn == None :
        print("Failed connection with database")
    else :
        cur=conn.cursor()
        try:
            #inserting information about a log
            sql=('''INSERT INTO ai_prompt(user_id,prompt,response,response_time) VALUES(?,?,?,?)''')
            cur.execute(sql,(user_id,prompt,response,response_time))
            conn.commit()
        except sqlite3.Error:
            print("Insertion of prompt failed")
        finally:
          conn.close()