import re
import sqlite3
from pathlib import Path
from app_model.hashing import generate_hash,is_valid_hash
from app_model.db import get_connection
#Inserting user details into database
def add_user (email,username,password_hash):
    conn=get_connection()
    #conditional statement to check if connection has been established
    if conn == None :
        print("Failed connection with database")
    else :
        cur=conn.cursor()
        #preventing an error just incase the username is already taken
        try:
            #inserting information about new user
            sql=('''INSERT INTO users(email,username,password_hash) VALUES(?,?,?)''')
            cur.execute(sql,(email,username,password_hash))
            conn.commit()
        except sqlite3.IntegrityError:
            print("Username is already taken")
        conn.close()
#Fetching all users
def get_all_users():
    conn=get_connection()
    #to check if communication with database has been established
    if conn == None :
        print("Failed connection with database")
    else :
        #declaration of emply users list
        users=[]
        #in the event of an error when fetching users the empty list is returned
        try:
          cur=conn.cursor()
          cur.execute("SELECT * FROM users")
          users=cur.fetchall()
        finally:
          conn.close()
        return users
#Fetching one user
def get_user(username):
    conn=get_connection()
    #to check if connection with database has been established
    if conn == None :
        print("Failed connection with database")
    else :
        cur=conn.cursor()
        cur.execute("SELECT*FROM users WHERE username=?",(username,))
        user=cur.fetchone()
        #Checking if user was found or not
        if user==None:
            print("User does not exists")
        else:
            print("User data retrieved")
        conn.close()
        return user
#Update password
def update_password(username,newpswhash):
    conn = get_connection()
    #checking if connection to database has been established
    if conn == None :
        return False
    else :
        try:
            cur=conn.cursor()
            cur.execute("UPDATE users SET password_hash = ? WHERE username = ?;", (newpswhash, username))
            conn.commit()
            conn.close()
            return True
        except Exception:
            conn.close()
            return False  
#Update email
def update_email(username,newemail):
    conn = get_connection()
    #checking if connection to database has been established
    if conn == None :
        return False
    else :
        try:
            cur = conn.cursor()
            cur.execute("UPDATE users SET email = ? WHERE username = ?;", (newemail, username))
            conn.commit()
            conn.close()
            return True
        except Exception :
            conn.close()
            return False    
#Updating name
def update_user(old_name, new_name):
    conn = get_connection()
    #checking if connection to database has been established
    if conn == None :
        return False
    else :
        cur = conn.cursor()
        cur.execute("UPDATE users SET username = ? WHERE username = ?", (new_name, old_name))
        conn.commit()
        #Checking if username actually exist and printing out result
        if cur.rowcount==0 :
            update=False
        else :
           update=True
        conn.close()
        return update
#Delete user from database
def delete_user(username):
    conn=get_connection()
    #checking if connection to database has been established
    if conn == None :
        return False
    else :
        cur=conn.cursor()
        cur.execute("DELETE FROM users WHERE username=? ",(username,))
        conn.commit()
        #Checking if username actually exist and printing out result
        if cur.rowcount==0:
            conn.close()
            return False
        else :
            conn.close()
            return True
        

            
#checking if password is strong enough
def check_password_intensity(psw):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$"
    #checks if password satdify the conditios of 8characters ,1 uppercase,1lowercase,1special character
    if re.match(pattern,psw):
        return True
    return False   
#Function to register users
def register_user(email,username, psw,confirm):
    if get_user(username) is not None:
        return "Username already exists. Please choose another one."
    # Check password strength
    if not check_password_intensity(psw): 
        return "Weak Password! Please use a stronger one with at least 8 characters with at least 1 uppercase,1lowercase and 1 special character"
    if psw != confirm :
        return "Correct your password it does not match"
    # If passes checks, hash and save
    hashed = generate_hash(psw)
    add_user(email,username, hashed)
    return True

#Function to login
def login_user(username, psw):
    user_data = get_user(username)
    if user_data:
        id,email, user_name, psw_hash, role = user_data
        if username == user_name and is_valid_hash(psw, psw_hash):
            return True
    return False
    

     
