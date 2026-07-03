import pandas as pd
import sqlite3
from app_model.db import get_connection
#Creates the users table if it does not already exist
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
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user'
                );'''
            cur.execute(sql) 
            print("Table succesfully created")
            conn.commit()
        except sqlite3.Error():
            print("Could not create table check if database is not on read mode only")
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
