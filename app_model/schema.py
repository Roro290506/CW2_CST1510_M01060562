import pandas as pd
import sqlite3
from app_model.db import get_connection
#Creates the aiprompt table if it does not already exist
def create_aiprompts():
    conn=get_connection()
    if conn==None:
        print("Database connection failed")
    else:
        #creation of table and columns
        try:
            cur=conn.cursor()
            sql='''CREATE TABLE IF NOT EXISTS ai_prompt(
                prompt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER ,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                prompt TEXT NOT NULL,
                response TEXT NOT NULL,
                response_time INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id) )
            '''
            cur.execute(sql) 
            print("Table succesfully created")
            conn.commit()
        except sqlite3.Error :
            print("Could not create the table")
        finally:
          conn.close()
            
 # create a logs table if not exist  
def create_logs_table():
    conn=get_connection()
    if conn== None:
        print("Database connection failed")
    else:
        try:
            cur=conn.cursor()
            sql='''CREATE TABLE IF NOT EXISTS logs(
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER FOREIGNKEY,
                login_time TIMESTAMP,
                logout_time TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) )'''
            cur.execute(sql) 
            print("Table successfully created")
            conn.commit()
        except sqlite3.Error :
            print("Could not create the table")
        finally:
         conn.close()
def create_user_table():
    conn = get_connection()
    #checking if the connection with db has been established
    if conn == None :
        print("Failed connection with database")
    else :
        try:
            cur = conn.cursor()
            sql = '''CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user'
                );'''
            cur.execute(sql) 
            print("Table succesfully created")
            conn.commit()
        except sqlite3.Error():
            print("Could not create table check if database is not on read mode only")
        finally:
         conn.close()
#create the password reset database 
def password_reset():
    conn=get_connection()
    if conn==None:
        print("Failed connection with database")
    else:
        try:
            cur=conn.cursor()
            sql='''CREATE TABLE IF NOT EXISTS password_reset(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                token TEXT NOT NULL,
                time_created TIMESTAMP,
                expires_at TIMESTAMP,
                FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE)'''
            cur.execute(sql)
            conn.commit()
        except sqlite3.Error():
            print("Could not create table")
        finally:
         conn.close()
#Migrates cyber incidents CSV data into the SQLite database.
def migrate_cyber_incidents():
    conn = get_connection()
    if conn == None :
        print("Failed connection with database")
    else :
        try:
            data = pd.read_csv("DATA/cyber_incidents.csv")
            try:
                data.to_sql("cyber_incidents", conn, if_exists="replace", index=False)
                print("Successfully loaded cyber incidents to database")
            except sqlite3.Error :
                print("Could not load the cyber incidents to database")
        except FileNotFoundError:
            print("Migration halted due to missing file")
        finally:
            conn.close()
#Migrates dataset metadata CSV data into the SQLite database.
def migrate_datasets_metadata():
    conn = get_connection()
    if conn == None :
        print("Failed connection with database")
    else :
        try:
           data = pd.read_csv("DATA/datasets_metadata.csv")
           try:
               data.to_sql("datasets_metadata", conn, if_exists="replace", index=False)
               print("Succesfully loaded datasets metadata into stabase")
           except sqlite3.Error :
               print("Could not load datasets metadata into database")
        except FileNotFoundError:
            print("Migration halted due to missing file")
        finally:
            conn.close()
#Migrates IT tickets CSV data into the SQLite database.
def migrate_it_tickets():
    conn = get_connection()
    if conn == None :
        print("Failed connection with database")
    else :
        try:
           data = pd.read_csv("DATA/it_tickets.csv")
           try:
              data.to_sql("it_tickets", conn, if_exists="replace", index=False)
              print("Succesfully loaded it tickets into database")
           except sqlite3.Error:
               print("Could not load it tickets into database")
        except FileNotFoundError:
            print("Migration halted because file is missing")
        finally:
            conn.close()
#Calling of functions
password_reset()
create_user_table()
migrate_cyber_incidents()
migrate_datasets_metadata()
migrate_it_tickets()
create_aiprompts()
create_logs_table()