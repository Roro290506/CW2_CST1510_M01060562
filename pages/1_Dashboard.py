import streamlit as st 
import datetime
from app_model.logic.logs import insert_log
#Dashboard setup
home=st.set_page_config(page_title="Home",page_icon="🏠",layout="wide")
#if not logged in it goes to Home pay
if "logged_in" not in st.session_state:
    st.session_state["logged_in"]=False
if not st.session_state["logged_in"]:
    st.warning("Please log in to access.")
    if st.button("Go To Log In"):
        st.session_state["logged_in"]=False
        st.switch_page('Home.py')
    st.stop()
else:
    st.success(f"You are logged in {st.session_state["username"]}")
st.title("🏠HOME DASHBOARD")
#Dashboard text
st.header(f"Welcome {st.session_state["username"]}")
st.markdown('''Datasets have been successfully retrieved from the database and are ready for analysis. 
            Use this workspace to synthesize cyber incident reports, IT ticket histories, and dataset metadata into a single, cohesive view. 
            Everything you need is fully loaded and available below. ''')
#Buttons to select to see the datasets
left_co,cent_co,last_co=st.columns([1,2,1])
with cent_co:
    if st.button("All Datasets",use_container_width=True):
        st.session_state["Selected"]="All"
        st.switch_page("pages/2_Analytics.py")
    if st.button("Cyber Incidents Data ", use_container_width=True):
         st.session_state["Selected"]="Cyber Incidents Data "
         st.switch_page("pages/2_Analytics.py")  
    if st.button("IT Tickets Data", use_container_width=True):
        st.session_state["Selected"]="IT Tickets Data "
        st.switch_page("pages/2_Analytics.py")
    if st.button("Datasets Metadata ", use_container_width=True):
        st.session_state["Selected"]="Datasets Metadata "
        st.switch_page("pages/2_Analytics.py")
#sidebar to switch to other pages and as well as logout       
with st.sidebar:
    if st.button("📊 Analytics Dashboard",use_container_width=True):
        st.switch_page("pages/2_Analytics.py")
    if st.button("👤 View My Profile", use_container_width=True):
        st.switch_page("pages/3_Profile.py")
    if st.button("🤖 Chat with GPT", use_container_width=True):
        st.switch_page("pages/4_ai_chat.py")
    #insert log details into the log table
    if st.button("🚪 Log Out", use_container_width=True):
        logout=datetime.datetime.now()
        insert_log(st.session_state["user_id"],st.session_state["login_time"],logout)
        st.session_state.messages=[]
        st.session_state["email"]=None
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.switch_page("Home.py")
    

     
    




