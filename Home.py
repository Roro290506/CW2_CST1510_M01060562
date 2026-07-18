import streamlit as st 
import datetime
import time
import secrets
from app_model.hashing import generate_hash
from app_model.users import login_user,register_user,get_all_users,insert_reset,get_token,check_password_intensity,update_password,delete_record,delete_token
from app_model.email_service import send_welcome_email,send_reset_email,send_successpsw_update
#configuration of page
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)
#the page title
st.title("Welcome to main page🏠")
#initializing of logged_in state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"]=False

#if logged in it displays this on Home page
if st.session_state["logged_in"]==True:
    st.success(f"You are logged in  {st.session_state["username"]}")
    if st.button("Go To DashBoard"):
        st.switch_page("pages/1_Dashboard.py")
else:
 #if not logged in this is what it displays
 #checks if there is a token in link if so it displays this first  for password reset if yu got the link 
 if "token" in st.query_params:
    #extraction of the token from the link
    user_token=st.query_params.get("token")
    #function of deleting token if time has lapsed
    delete_record()
    #checking if the token exist in password reset table and if yes it returns the token record
    result=get_token(user_token)
    if result != None:
        #extraction of the email from the record
        email=result[1]
        #asking for user input for new password and confimation
        new_password = st.text_input("New Password", type="password", key="register_psw")
        confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_psw")
        if st.button("Change Password"):
            #checks if password match
            if new_password != confirm_password:
                st.error("The two passwords are not the same ")
                st.stop()
            #checks if password is strong
            if check_password_intensity(new_password)==False:
                st.error("Weak Password! Please use a stronger one with at least 8 characters with at least 1digit, 1uppercase,1lowercase and 1 special character")    
                st.stop()
            #extraction of all users from the table of users
            users=get_all_users()
            #checks if the email matches any stored in the database
            for user in users:
                db_id,db_email,db_name,db_hash,db_role=user
                if email==db_email :
                    username=db_name
                    break   
            #if so then a new hash is generated 
            new_password_hash=generate_hash(new_password)
            #calls function to update the password
            success=update_password(username,new_password_hash)
            #displays messages depending if it was succesful
            if success== True:
                send_successpsw_update(db_email,db_name)
                st.success("Password Reset was successful")
                #deleting token since it has already been used
                delete_token(user_token)
                time.sleep(2)
                st.query_params.clear()
                st.rerun()
            else:
                st.error("Password Reset Failed. Try Again Later.") 
    #link has expired or invalid       
    else:
                st.error("Invalid or expired token link.")

 #Creation for tabs for login and register
 tab_login, tab_register=st.tabs(["Login Status","Register"])
 
 #login tab
 with tab_login:
     #Ask user to enter credentials
    login_username=st.text_input("Username",key="login_username").strip()
    login_password=st.text_input("Password",type="password",key="login_password")
    #option to change password via email if you have forgotten about it
    with st.expander("Forgot Password ?"):
        email=st.text_input("Enter your email address",key="Recovery_email")
        if st.button("Continue",key="Continue",use_container_width=True):
            users=get_all_users()
            found=False
            for user in users:
                db_id,db_email,db_name,db_hash,db_role=user
                if db_email==email:
                    found=True 
                    break
            #next steps after the email is found
            if found:
                #token generation
                token=secrets.token_urlsafe(16)
                #current time variable
                time_created=datetime.datetime.now()
                #time when token expires
                expires_at=time_created + (datetime.timedelta(minutes=15))
                #inserting token details in password rest table
                insert_reset(email,token,time_created,expires_at)
                #cration of token link
                reset_link = f"http://localhost:8501/?token={token}"
                #function to send email with link and variable to store returned boolean
                reset=send_reset_email(db_email,db_name,reset_link)
                #Updating user what is happening
                if reset:
                    st.success("Email to reset password has been sent")
                else:
                    st.error("Try again later")   
            else:
                st.error("Email does not exist in our database")
    #if everything is correct the session state["logged in"] is updated after clicking button}
    if st.button("Log In"):
        st.session_state["logged_in"]=login_user(login_username,login_password) 
        #if logged in then the session state are updated and user is switched  to the Dashboard
        if st.session_state["logged_in"]:
            st.session_state["username"]=login_username
            usersdict=get_all_users()
            for user in usersdict:
                db_id,db_email,db_name,db_hash,db_role=user
                if db_name==login_username:
                    st.session_state["user_id"]=db_id
                    st.session_state["email"]=db_email
                    st.session_state["role"]=db_role
                    st.session_state["login_time"]=datetime.datetime.now()
            st.success("Logged in successfully")
            st.switch_page("pages/1_Dashboard.py")
        else:
            st.error("Wrong Password or Username")
   
#the registering tab 
 with tab_register:
     #ask user to enter the following details
    email=st.text_input("Gmail",key="email_input")
    register_username = st.text_input("New Username", key="register_username").strip()
    register_password = st.text_input("New Password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_password")
    #if you press the register button checks if the details meet the requirements
    if st.button("Register"):
        st.session_state["logged_in"] = False
        result = register_user(email,register_username, register_password,confirm_password)
        if result == True:
            welcome=send_welcome_email(register_username,email)
            if welcome:
                st.success("Registration email sent")
            else:
                st.success("Registration email failed but you are registered")
            st.success("Registration successful! You can now log in.")
        else:
            # Display whatever error string was returned from the function
            st.error(result)
 st.session_state["Edit_username"]=False
 st.session_state["Edit_email"]=False
 st.session_state["Edit_psw"]=False
 st.session_state["psw_verified"] = False

