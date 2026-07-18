import re
import datetime
import sqlite3
from pathlib import Path
from app_model.hashing import generate_hash,is_valid_hash
from app_model.db import get_connection

#delete token record because execution is done
def delete_token(token):
    #establishing connection to database
    conn=get_connection()
    if conn == None :
        return False
    else :
      #execution
      try:
        cur=conn.cursor()
        cur.execute('DELETE FROM password_reset WHERE token = ?', (token,))
        conn.commit()
      finally:
        conn.close()

#delete token record because the time has lapsed
def delete_record():
    #establishing connection to database
    conn=get_connection()
    if conn == None :
        print("Connection to database failed")
    else :
        #Execution
        try:
           cur=conn.cursor()
           #variable to store current time
           CURRENT_TIMESTAMP=datetime.datetime.now()
           cur.execute('DELETE FROM password_reset WHERE expires_at < ?',(CURRENT_TIMESTAMP,))
           conn.commit()
           return True
        except sqlite3.OperationalError:
            print("Failed to delete")
        finally:
           conn.close()
        
#Fetch the token record
def get_token(token):
    conn=get_connection()
    if conn==None:
        print("Connection to database failed")
    else:
        cur=conn.cursor()
        cur.execute("SELECT*FROM password_reset where token=?",(token,))
        record=cur.fetchone()
        conn.close()
        return record
#inserting tuple into password reset 
def insert_reset(email,token,time_created,expires_at):
    conn=get_connection()
    if conn==None :
        print("Connenction to db failed")
    else:
        cur=conn.cursor()
        try:
            sql=('''INSERT INTO password_reset(email,token,time_created,expires_at)VALUES(?,?,?,?)''')
            cur.execute(sql,(email,token,time_created,expires_at))
            conn.commit()
        except sqlite3.Error():
            print("failed to add")
        finally:
            conn.close()     
#Inserting user details into database
def add_user (email,username,password_hash):
    conn=get_connection()
    #conditional statement to check if connection has been established
    if conn == None :
        print("Failed connection with database")
    else :
        cur=conn.cursor()
        #preventing an error just incase the username or email is already taken
        try:
            #inserting information about new user
            sql=('''INSERT INTO users(email,username,password_hash) VALUES(?,?,?)''')
            cur.execute(sql,(email,username,password_hash))
            conn.commit()
        except sqlite3.IntegrityError:
            print("Username is already taken")
        finally:
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
        return "Failed to connect to db"
    else :
       try:
        cur = conn.cursor()
        cur.execute("UPDATE users SET username = ? WHERE username = ?", (new_name, old_name))
        conn.commit()
        #Checking if username actually exist and printing out result
        if cur.rowcount==0 :
            update="Not Updated"
        else :
           update="Updated"
        conn.close()
        return update
       except sqlite3.IntegrityError: 
           return "Username exist already"
           
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
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$"
    #checks if password satdify the conditions of 8characters ,1 uppercase,1lowercase,1special character,1digit
    if re.match(pattern,psw):
        return True
    return False   
#checking if it is gmail email entered
def is_gmail(email):
    #preventing falsy string
    if not email:
        return False
    #putting everything lowercase and deleting empty space
    email=email.lower().strip()
    if "@" in email and email.endswith("@gmail.com"):
        #ensuring there is something before the @gmail.com
        name=email.split("@")[0]
        if len(name)>0:
            return True   
    return False
#Function to register users for the database
def register_user(email,username, psw,confirm):
    if not is_gmail(email):
        return"Enter a gmail account"   
    if not username:
        return" Enter a username"
    if get_user(username) is not None:
        return "Username already exists. Please choose another one."
    # Check password strength
    if not check_password_intensity(psw): 
        return "Weak Password! Please use a stronger one with at least 8 characters with at least 1 digit, 1 uppercase,1lowercase and 1 special character"
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
#FLATFILE SYSTEM STORED
#function to check if there is no similar username 
def similar_username(username):
    #variable to store boolean value for similarity in usernames
    similar1=False
    try:
     #opening the file for read
     with open("DATA/users.txt","r") as f :
        users=f.readlines()
        for user in users :
            #skips if there is a blank line onto next line
            if not user.strip() :
                continue
            #stops program from crashing in the event that details of a user l typed in manually and failed to add coma for separation
            try :
               username1,password=user.strip().split(",")
            except ValueError:
                continue
            #conditional statement to exit loop after there is similarity noted
            if username == username1:
                similar1=True
                break
     return similar1
    except FileNotFoundError:
        return False

#register user for textfile
def register_user_txt():
    print("Welcome New User!!")
    #Prompting user to enter username
    username=input("Enter a username :").strip()
    #Checks if DATA folder exists if not its created
    Path("DATA").mkdir(exist_ok=True)
    file_path = Path("DATA/users.txt")
    #checking if the username already exists and if so prompted to enter again
    if file_path.exists():
       similar=similar_username(username)
       if similar==True:
        while similar == True :
            print("Username already exists enter a new one ")
            username=input("Enter a username: ").strip()
            similar=similar_username(username)
    while True:
        psw = input("Create a password with at least 8 characters, 1 digit, 1 special character, 1 lowercase and 1 uppercase: ")
        #checks if password is strong enough
        while not check_password_intensity(psw):
            psw = input("Re-enter a password meeting all requirements of 8 characters, 1 special character, 1 lowercase,1 digit and 1 uppercase : ")
        #promting user to confirm their password and checking if it matches
        confirm = input("Confirm your password: ")
        if psw == confirm:
            break 
        else:
            print(" Your passwords do not match. Please start over.") 
    #generation of hash
    hashed_psw=generate_hash(psw)
    #appending the username and password to file
    with open("DATA/users.txt","a")as f:
        f.write(f"{username},{hashed_psw}\n")
    print("User succesfully registered ! ")

#Function to login textfile
def login_user_txt():
    #Prompting user to enter username and password
    username=input("Enter your username:").strip()
    psw=input("Enter your password: ")
    #trying to open the textfile and look for the username and checking if password is correct
    try :
     result=False
     with open("DATA/users.txt","r") as f :
        for line in f:
            #skips line in the event of not following the correct format
            try :
               username1,hashed=line.strip().split(",")
            except ValueError :
                continue
            #checking if the username are exactly the same
            if username1==username :
                result=is_valid_hash(psw,hashed)
                break
    except FileNotFoundError: 
        print("File not found")
    return result 

    

     
