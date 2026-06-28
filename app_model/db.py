import sqlite3
def get_connection():
    conn=sqlite3.connect("DATA/project_data.db")
    return(conn)