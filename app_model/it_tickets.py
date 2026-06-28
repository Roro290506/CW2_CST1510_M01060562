import pandas as pd
from app_model.db import get_connection
#Querying SQLite to a Dataframe
def get_all_it_tickets():
    conn=get_connection()
    sql=("SELECT*FROM it_tickets")
    data=pd.read_sql(sql,conn)
    conn.close
    return(data)