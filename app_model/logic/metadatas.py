import pandas as pd
from app_model.db import get_connection
def get_all_datasets_metadata():
    conn=get_connection()
    sql=("SELECT*FROM datasets_metadata")
    data=pd.read_sql(sql,conn)
    conn.close
    return(data)