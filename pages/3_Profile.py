import streamlit as st
from app_model.hashing import generate_hash
from app_model.users import update_user,check_password_intensity,update_email,update_password,delete_user
st.set_page_config(page_title="User Profile", page_icon="👤", layout="wide")
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in to access your profile.")
    if st.button("Go To Log In"):
        st.switch_page('Home.py')
    st.stop()
st.title(f"👤 {st.session_state["username"]}")
st.header("Account & Settings")
st.write("Username")
st.write(f"{st.session_state["username"]}")
if st.button("Edit"):
    new_username=st.text_input("Change your username",key="new_username").strip()
    if st.button("Update Username"):
      update=update_user(st.session_state["username"],new_username)
      if update :
        st.session_state["username"]=new_username
        st.success("Username succesfully changed!!")
      else :
        st.error("Username update failed!!")

new_password=st.text_input("Change Password",key="new_password",type="password")
confirm=st.text_input("Confirm Password",key="confirm",type="password")
if st.button("Update Password"):
    if not check_password_intensity(new_password): 
        st.error("Weak Password! Please use a stronger one with at least 8 characters with at least 1 uppercase,1lowercase and 1 special character")
    if new_password != confirm :
        st.error("Correct your password it does not match")
    # If passes checks, hash and save
    hashed = generate_hash(new_password)
    update=update_password(st.session_state["username"],hashed)
    if update:
        st.success("Password successfully changed")
    else:
        st.error("Password was not updated try again")
new_email=st.text_input("Change your email",key="email").strip()
if st.button("Update Email"):
    update=update_email(st.session_state["username"],new_email)
    if update :
        st.success("Email succesfully changed!!")
    else :
        st.error("Email update failed!!")
account=st.selectbox("Do you want to delete account",["No","Yes"])  
if account == "Yes":
    delete=delete_user(st.session_state["username"])
    if delete:
        st.success("Account successfully deleted!!")
        st.switch_page("Home.py")
    else:
        st.error("Try again account was not deleted")
if st.button("Return To Dashboard"):
    st.switch_page("pages/1_Dashboard.py")
    
    

    

    
    