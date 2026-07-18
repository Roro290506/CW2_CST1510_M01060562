import streamlit as st
import pandas as pd
from app_model.users import get_all_users
from app_model.logic.logs import get_all_logs
from app_model.logic.ai_prompt import get_all_prompt
if st.session_state.get("logged_in") and st.session_state["role"] == "admin":
    st.title("Admin 🔑 👤 💬")
    
    #Displaying of user table 
    st.subheader("Users Table")
    userdata=get_all_users()
    datadf=pd.DataFrame(userdata,columns=["user_id","email","username","password_hash","role"])
    datadisplay=datadf.drop(columns="password_hash")
    st.dataframe(datadisplay)
    #Displaying of logs table
    st.subheader("User Logs Table")
    logdata=get_all_logs()
    logdf =pd.DataFrame(logdata,columns=["log_id","user_id","login_time","logout_time"])
    st.dataframe(logdf)
    #Displaying of AI prompt table
    st.subheader("AI Prompts Table")
    promptdata=get_all_prompt()
    promptdf=pd.DataFrame(promptdata,columns=["prompt_id","user_id","time","prompt","response","response time in ms"])
    st.dataframe(promptdf)
    
    if st.button("Go To DashBoard",use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")
else:
    #The admin page for normal user
    st.title("ACCESS DENIED")
    st.error("You do not have permission to view this page")
    if st.button("Go To DashBoard",use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")