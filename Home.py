import streamlit as st 
from app_model.users import login_user,register_user
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

st.title("Welcome to main page🏠")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"]=False

tab_login, tab_register=st.tabs(["Login Status","Register"]) 

with tab_login:
    login_username=st.text_input("Username",key="login_username").strip()
    login_password=st.text_input("Password",type="password",key="login_password")
    if st.button("Log In"):
        st.session_state["logged_in"]=login_user(login_username,login_password) 
        if st.session_state["logged_in"]:
            st.session_state["username"]=login_username
            st.success("Logged in successfully")
            st.switch_page("pages/1_Dashboard.py")
        else:
            st.error("Wrong Password or Username")
    

with tab_register:
    email=st.text_input("Email",key="email")
    register_username = st.text_input("New Username", key="register_username").strip()
    register_password = st.text_input("New Password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_password")
    if st.button("Register"):
        st.session_state["logged_in"] = False
        result = register_user(email,register_username, register_password,confirm_password)
        if result == True:
            st.success("Registration successful! You can now log in.")
        else:
            # Display whatever error string was returned from the function
            st.error(result)

#st.session_state
   