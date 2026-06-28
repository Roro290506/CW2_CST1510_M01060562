import pandas as pd
from app_model.db import get_connection
#Creates the users table if it does not already exist
def create_user_table():
    conn = get_connection()
    cur = conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user'
            );'''
    cur.execute(sql) 
    conn.commit()
    conn.close()
#Migrates cyber incidents CSV data into the SQLite database.
def migrate_cyber_incidents():
    conn = get_connection()
    data = pd.read_csv("DATA/cyber_incidents.csv")
    data.to_sql("cyber_incidents", conn, if_exists="replace", index=False)
    conn.close()
#Migrates dataset metadata CSV data into the SQLite database.
def migrate_datasets_metadata():
    conn = get_connection()
    data = pd.read_csv("DATA/datasets_metadata.csv")
    data.to_sql("datasets_metadata", conn, if_exists="replace", index=False)
    conn.close()
#Migrates IT tickets CSV data into the SQLite database.
def migrate_it_tickets():
    conn = get_connection()
    data = pd.read_csv("DATA/it_tickets.csv")
    data.to_sql("it_tickets", conn, if_exists="replace", index=False)
    conn.close()