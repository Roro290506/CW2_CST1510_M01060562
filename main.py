import bcrypt
from pathlib import Path
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
     with open("users.txt","r") as f :
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
    file_path=Path("users.txt")
    if file_path.exists():
       similar=similar_username(username)
       if similar==True:
        while similar == True :
            print("Username already exists enter a new one ")
            username=input("Enter a username :")
            similar=similar_username(username)
    psw=input("Create a password with at least 12 characters :")
    while len(psw) < 12 :
       psw=input("Reenter a password with at least 12 characters :") 
    confirm=input("Confirm your password :")    
    while psw != confirm :
        print("Your passwords do not match :")  
        psw=input("Create a password with at least 12 characters :")
        while len(psw) >= 12 :
          psw=input("Reenter a password with at least 12 characters :") 
        confirm=input("Confirm your password :") 
    hashed_psw=generate_hash(psw)
    with open("users.txt","a")as f:
        f.write(f"{username},{hashed_psw}\n")
try :
 register_user()
 register_user()
except FileNotFoundError :
    print("file not found")
    
    
    
            
            
            
    