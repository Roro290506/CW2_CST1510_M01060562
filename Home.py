import streamlit as st 
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
    
    if st.button("Log In"):
        st.session_state["logged_in"]=True
    
with tab_register:
    if st.button("Register"):
        st.session_state["logged_in"]=False

st.session_state
   