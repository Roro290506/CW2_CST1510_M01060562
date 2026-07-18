import streamlit as st
import time
from app_model.users import is_gmail
from app_model.email_service import send_delete_update,send_successpsw_update
from app_model.hashing import generate_hash,is_valid_hash
from app_model.users import update_user,check_password_intensity,update_email,update_password,delete_user,get_user
st.set_page_config(page_title="User Profile", page_icon="👤", layout="wide")
#can't see anything if not logged in
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in to access your profile.")
    if st.button("Go To Log In"):
        st.switch_page('Home.py')
    st.stop()
st.title(f"👤 {st.session_state["username"]}")
st.header("Account & Settings")
#function to change username 
with st.container() :
    if st.session_state["Edit_username"] is True:
        newusername=st.text_input("Enter new username")
        col_button1,col_button2=st.columns([1,1])
        with col_button1:
            if st.button("Update",key="Update"):
              if newusername:
                update=update_user(st.session_state["username"],newusername)
                if update=="Updated":
                   st.session_state["username"]=newusername
                   st.success("Username succesfully updated")
                elif update=="Not Updated":
                    st.error("Username not updated")
                elif update== "Username exist already":
                    st.error("Username already exists")
                else:
                    st.error("Failed connection with database try later")
              else:
                  st.error("Enter a username")
              st.session_state["Edit_username"]=False
              time.sleep(1)
              st.rerun()
        with col_button2:
            if st.button("Cancel",key="Cancel"):
               st.session_state["Edit_username"]=False     
               st.rerun()      
    else:
        col1,col2=st.columns([4,1])
        with col1:
            st.caption("Username")
            st.write(f"{st.session_state["username"]}")
        with col2:
            if st.button("Edit",key="Edit"):
              st.session_state["Edit_username"] = True  
              st.rerun()
#Function to change email             
with st.container() :
    if st.session_state["Edit_email"] is True:
        newemail=st.text_input("Enter new email")
        col_button1,col_button2=st.columns([1,1])
        with col_button1:
            if st.button("Update",key="Update_email"):
                if is_gmail(newemail):
                  update=update_email(st.session_state["username"],newemail)
                  if update:
                   st.session_state["email"]=newemail
                   st.success("Email succesfully updated")
                  else:
                    st.error("Email not updated it already exists")
                else:
                    st.error("Enter a gmail ")
                st.session_state["Edit_email"]=False
                time.sleep(1)
                st.rerun()
        with col_button2:
            if st.button("Cancel",key="Cancel_update"):
               st.session_state["Edit_email"]=False     
               st.rerun()      
    else:
        col1,col2=st.columns([4,1])
        with col1:
            st.caption("Email")
            st.write(f"{st.session_state["email"]}")
        with col2:
            if st.button("Edit",key="Edit_"):
              st.session_state["Edit_email"] = True  
              st.rerun()             
#Function to change password             
with st.container():
    if st.session_state.get("Edit_psw") is True:
        psw = st.text_input("Enter your current password", type="password",key="Current_psw")
        if st.button("Check Password", key="Check_psw"):
            pswhash = get_user(st.session_state["username"])[3]
            if is_valid_hash(psw, pswhash):
                st.session_state["psw_verified"] = True
            else:
                st.session_state["psw_verified"] = False
                st.error("Incorrect password")
                time.sleep(1)
                st.rerun()
        if st.session_state["psw_verified"]:
            st.success("Password is correct, you can proceed")
            st.write("Please use a stronger one with at least 8 characters with at least 1 digit, 1 uppercase, 1 lowercase and 1 special character")
            newpsw = st.text_input("Enter new password", type="password", key="newpsw_input")
            confirm = st.text_input("Confirm", type="password", key="confirm_input")
            if st.button("Update", key="Update_psw"):
                if newpsw != confirm:
                    st.error("The two passwords are different")
                elif not check_password_intensity(newpsw):
                    st.error("Weak Password! Please use a stronger one with at least 8 characters with at least 1 digit, 1 uppercase, 1 lowercase and 1 special character")
                else:
                    newpswhash = generate_hash(newpsw)
                    if update_password(st.session_state["username"], newpswhash):
                        send_successpsw_update(st.session_state["email"],st.session_state["username"])
                        st.success("Password successfully updated")
                        st.session_state["Edit_psw"] = False
                        st.session_state["psw_verified"] = False
                    else:
                        st.error("Password not updated, try again later")
                    time.sleep(1)
                    st.rerun()
    else:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.caption("Password")
            st.write("...............")
        with col2:
            if st.button("Edit", key="Edit_psw_btn"):
                st.session_state["Edit_psw"] = True
                st.session_state["psw_verified"] = False
                st.rerun()
                
 #Function to delete account            
account=st.selectbox("Do you want to delete account",["No","Yes"])  
if account == "Yes":
    delete=delete_user(st.session_state["username"])
    if delete:
        send_delete_update(st.session_state["email"],st.session_state["username"])
        st.success("Account successfully deleted!!")
        time.sleep(1)
        st.session_state["logged_in"]=False
        st.switch_page("Home.py")
    else:
        st.error("Try again account was not deleted")
if st.button("Return To Dashboard"):
    st.switch_page("pages/1_Dashboard.py")
    
    

    

    
    