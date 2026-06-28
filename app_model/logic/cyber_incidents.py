import pandas as pd
from app_model.db import get_connection

def get_all_cyber_incidents():
    conn = get_connection()
    sql = ("SELECT * FROM cyber_incidents")
    data = pd.read_sql(sql, conn)
    conn.close()
    return data