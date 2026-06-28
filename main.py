import bcrypt
from pathlib import Path
import sqlite3,pandas as pd
#Create database
conn=sqlite3.connect("DATA/project_data.db")
cur=conn.cursor()
#Creation of TABLE
def create_user_table (conn):
    cur=conn.cursor()
    sql=('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                             username TEXT NOT NULL UNIQUE,
                                             password_hash TEXT NOT NULL,
                                             role TEXT DEFAULT 'user');''')
    cur.execute(sql) ; conn.commit
#Inserting values into the table
def add_user (conn,username,password_hash,role="user"):
    cur=conn.cursor()
    sql=('''INSERT INTO users(username,password_hash,role) VALUES(?,?,?)''')
    cur.execute(sql,(username,password_hash,role)) ; conn.commit()
#Fetching all users
def get_all_users(conn):
    cur=conn.cursor()
    cur.execute("SELECT * FROM users")
    return cur.fetchall()
#Fetching one user
def get_user(conn,username):
    cur=conn.cursor()
    cur.execute("SELECT*FROM users WHERE username=?",(username,))
    return cur.fetchone()
#UPDATE
def update_user(conn,old_name,new_name):
    cur=conn.cursor()
    cur.execute("UPDATE users SET username=? WHERE username=?",(new_name,old_name))
    conn.commit()
#Delete user from database
def delete_user(conn,username):
    cur=conn.cursor()
    cur.execute("DELETE FROM users WHERE username=? ",(username,))
    conn.commit()
#CSV to sqlite migration using pandas
def migrate_cyber_incidents(conn):
    data=pd.read_csv("DATA/cyber_incidents.csv")
    data.to_sql("cyber_incidents",conn)
#CSV to sqlite for metadata
def migrate_datasets_metadata(conn):
    data=pd.read_csv("DATA/datasets_metadata.csv")
    data.to_sql("datasets_metadata",conn) 
#it tickects to db 
def migrate_it_tickets(conn):
    data=pd.read_csv("DATA/it_tickets.csv")
    data.to_sql("it_tickets",conn) 
#Querying SQLite to a Dataframe
def get_all_cyber_incidents(conn):
    sql=("SELECT*FROM cyber_incidents")
    data=pd.read_sql(sql,conn)
    conn.close
    return(data)
def get_all_datasets_metadata(conn):
    sql=("SELECT*FROM datasets_metadata")
    data=pd.read_sql(sql,conn)
    conn.close
    return(data)
def get_all_it_tickets(conn):
    sql=("SELECT*FROM it_tickets")
    data=pd.read_sql(sql,conn)
    conn.close
    return(data)
print(get_all_cyber_incidents(conn))
print(get_all_it_tickets(conn))
print(get_all_datasets_metadata(conn))
conn.close
#generation pf the password hash
def generate_hash(psw):
    psw_byte=psw.encode("utf-8")
    salt=bcrypt.gensalt()
    hashed=bcrypt.hashpw(psw_byte,salt)
    return hashed.decode("utf-8")
#checking if password == to the hash stored
def is_valid_hash(psw,hashed):
    hash_=hashed.encode("utf-8")
    psw_bytes=psw.encode("utf-8")
    is_valid=bcrypt.checkpw(psw_bytes,hash_)
    return is_valid
#Function to check if username does not exist in the database already
def similar_username(username):
    similar1=False
    try:
     with open("DATA/users.txt","r") as f :
        users=f.readlines()
        for user in users :
            if not user.strip() :
                continue
            username1,password=user.strip().split(",")
            if username == username1:
                similar1=True
                break
     return similar1
    except FileNotFoundError:
        return False
#Function to register users
def register_user():
    username=input("Enter a username :")
    file_path=Path("DATA/users.txt")
    if file_path.exists():
       similar=similar_username(username)
       if similar==True:
        while similar == True :
            print("Username already exists enter a new one ")
            username=input("Enter a username: ")
            similar=similar_username(username)
    psw=input("Create a password with at least 12 characters :")
    while len(psw) < 12 :
       psw=input("Reenter a password with at least 12 characters :") 
    confirm=input("Confirm your password :")    
    while psw != confirm :
        print("Your passwords do not match ")  
        psw=input("Create a password with at least 12 characters :")
        while len(psw) <12 :
          psw=input("Reenter a password with at least 12 characters :") 
        confirm=input("Confirm your password :") 
    hashed_psw=generate_hash(psw)
    with open("DATA/users.txt","a")as f:
        f.write(f"{username},{hashed_psw}\n")
    print("User succesfully registered ! ")
#Function to login
def login_user():
    username=input("Enter your username:")
    psw=input("Enter your password: ")
    try :
     result=False
     with open("DATA/users.txt","r") as f :
        for line in f:
            username1,hashed=line.strip().split(",")
            if username1==username :
                result=is_valid_hash(psw,hashed)
                break
    except FileNotFoundError: 
        print("File not found")
    return result 
#Function to choose login,register  user or exit     
def main():
    while True:
        print("WElcome To The System!!")
        print('1. To Register\n2. To Log in\n3. To Exit')
        choice = input(': > ')
        
        if choice == '1':
            register_user() 
        elif choice == '2':
            print('Login successful!' if login_user() == True else 'Incorrect login.')
        elif choice == '3':
            print('Goodbye!')
            break

#if __name__ == '__main__':
    #main()



    
    
    
            
            
            
    