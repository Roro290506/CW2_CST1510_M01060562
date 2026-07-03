import streamlit as st 
import pandas as pd
from app_model.logic.cyber_incidents import get_all_cyber_incidents
home=st.set_page_config(page_title="Home",page_icon="🏠",layout="wide")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"]=False
if not st.session_state["logged_in"]:
    st.warning("Please log in to access.")
    st.stop()
else:
    st.success("You are logged in!")
     
    
st.title("Welcome to the Home Page")
data= get_all_cyber_incidents()

with st.sidebar:
    st.header("Navigation")
    severity_=st.selectbox('Severity Level',data["severity"].unique())
data["timestamp"]=pd.to_datetime(data["timestamp"])
filtered_data=data[data["severity"]==severity_]
st.subheader("Cyber Incidents Data Overview")

col1,col2=st.columns(2)
with col1:
   st.subheader("Cyber Incidents with Severity")
   st.bar_chart(filtered_data["category"].value_counts())
   
with  col2:
       st.subheader("Category Trend Over Time")
       st.line_chart(filtered_data,x="timestamp",y="category")
       
st.subheader("Filtered Data")
st.dataframe(filtered_data)


