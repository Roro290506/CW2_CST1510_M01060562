import re
import sqlite3
from pathlib import Path
from hashing import generate_hash,is_valid_hash
from app_model.db import get_connection
#Inserting user details into database
def add_user (username,password_hash,role="user"):
    conn=get_connection()
    #conditional statement to check if connection has been established
    if conn == None :
        print("Failed connection with database")
    else :
        cur=conn.cursor()
        #preventing an error just incase the username is already taken
        try:
            #inserting information about new user
            sql=('''INSERT INTO users(username,password_hash,role) VALUES(?,?,?)''')
            cur.execute(sql,(username,password_hash,role))
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
#Updating name
def update_user(old_name, new_name):
    conn = get_connection()
    #checking if connection to database has been established
    if conn == None :
        print("Failed connection with database")
    else :
        cur = conn.cursor()
        cur.execute("UPDATE users SET username = ? WHERE username = ?", (new_name, old_name))
        conn.commit()
        #Checking if username actually exist and printing out result
        if cur.rowcount==0 :
            print("Old Username does not exist in the database no updates were made.")
        else :
            print("The username was succesfully updated.")
        conn.close()
#Delete user from database
def delete_user(username):
    conn=get_connection()
    #checking if connection to database has been established
    if conn == None :
        print("Failed connection with database")
    else :
        cur=conn.cursor()
        cur.execute("DELETE FROM users WHERE username=? ",(username,))
        conn.commit()
        #Checking if username actually exist and printing out result
        if cur.rowcount==0:
            print("Username does not exist so there was nothing deleted")
        else :
            print("Successfully deleted")
        conn.close()

#Function to check if username does not exist in the database already
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
#checking if password is strong enough
def check_password_tensity(psw):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$"
    #checks if password satdify the conditios of 8characters ,1 uppercase,1lowercase,1special character
    if re.match(pattern,psw):
        return True
    return False   
#Function to register users
def register_user():
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
        psw = input("Create a password with at least 8 characters, 1 special character, 1 lowercase and 1 uppercase: ")
        #checks if password is strong enough
        while not check_password_tensity(psw):
            psw = input("Re-enter a password meeting all requirements of 8 characters, 1 special character, 1 lowercase and 1 uppercase : ")
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
#Function to login
def login_user():
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
     
