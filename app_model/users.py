import bcrypt
from pathlib import Path
from app_model.db import get_connection
#Inserting user details into database
def add_user (username,password_hash,role="user"):
    conn=get_connection()
    cur=conn.cursor()
    sql=('''INSERT INTO users(username,password_hash,role) VALUES(?,?,?)''')
    cur.execute(sql,(username,password_hash,role))
    conn.commit()
    conn.close()
#Fetching all users
def get_all_users():
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("SELECT * FROM users")
    users=cur.fetchall()
    conn.close()
    return users
#Fetching one user
def get_user(username):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("SELECT*FROM users WHERE username=?",(username,))
    user=cur.fetchone()
    conn.close()
    return user
#Updating name
def update_user(old_name, new_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET username = ? WHERE username = ?", (new_name, old_name))
    conn.commit()
    conn.close()
#Delete user from database
def delete_user(username):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("DELETE FROM users WHERE username=? ",(username,))
    conn.commit()
    conn.close()
#generation of the password hash
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