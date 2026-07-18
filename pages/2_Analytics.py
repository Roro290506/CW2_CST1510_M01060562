import streamlit as st 
import plotly.express as px
import pandas as pd
from app_model.logic.cyber_incidents import get_all_cyber_incidents
from app_model.logic.it_tickets import  get_all_it_tickets
from app_model.logic.metadatas import  get_all_datasets_metadata
if "logged_in" not in st.session_state:
    st.session_state["logged_in"]=False
if not st.session_state["logged_in"]:
    st.warning("Please log in to access.")
    if st.button("Go To Log In"):
        st.session_state["logged_in"]=False
        st.switch_page('Home.py')
    st.stop()


st.title("📊 Analytics Dashboard")
#function to display cyber incidents
def display_cyber_incidents():
     try:
      data= get_all_cyber_incidents()
      if data.empty:
          st.error("No data available for display at the moment")
      else:
       with st.sidebar:
        st.header("Cyber Incidents Navigation Bar")
        severity_=st.selectbox('Severity Level',data["severity"].unique())
        colors = {"Low": "🟢 Low",
                  "Medium": "🟡 Medium",
                  "High": "🟠 High",
                  "Critical": "🔴 Critical"
                 }
        st.markdown(f"### Current Status: {colors[severity_]}")
       data["timestamp"]=pd.to_datetime(data["timestamp"])
       filtered_data=data[data["severity"]==severity_]
       st.subheader("Cyber Incidents Data Overview")
       
       col1,col2=st.columns(2)
       with col1:
         st.subheader("Incidents Category Percentage")
         st.write(f"No of Incidents {filtered_data["incident_id"].count()}")
         fig = px.pie(
            filtered_data, 
            names="category"
         )
         st.plotly_chart(fig, use_container_width=True)
       with col2:
        st.subheader("Incidents Status Tally")
        st.bar_chart(filtered_data["status"].value_counts())
   
       st.subheader("Category Trend Over Time")
       st.line_chart(filtered_data,x="timestamp",y="category")
       
       st.subheader("Filtered Data")
       st.dataframe(filtered_data)
     except  Exception : 
        st.error("Database connection failed. Please try again later.")
#functions to display it tickets
def display_it_tickets():
     try:
      data=  get_all_it_tickets()
      if data.empty:
          st.warning("No data available for this selection at the moment")
      else:
       with st.sidebar:
        st.header("IT Tickets Navigation")
        assigned_to=st.selectbox('assigned_to',data["assigned_to"].unique())
       data["created_at"]=pd.to_datetime(data["created_at"])
       filtered_data=data[data["assigned_to"]==assigned_to]
       st.subheader("IT Tickets Data Overview")

       col1,col2=st.columns(2)
       with col1:
         st.header("Tickets Priority Percentage")
         st.write(f"No of Tickets {filtered_data["ticket_id"].count()}")
         fig=px.pie(
           filtered_data,
           names="priority"
         )
         st.plotly_chart(fig,use_container_width=True)
        
       with  col2:
         st.subheader("Tickets Status Tally")
         st.bar_chart(filtered_data["status"].value_counts())
          
       st.subheader("Status Over Time")
       st.line_chart(filtered_data,x="created_at",y="status")
       
       st.subheader("Filtered Data")
       st.dataframe(filtered_data)
     except Exception :
        st.error("Database connection failed. Please try again later.")
#functions to display metadata
def display_datasets_metadata():
     try:
      data=get_all_datasets_metadata()
      if data.empty:
          st.error("No data available for this section at the moment")
      else:
       st.header("Datasets Metadata Overview")
       
       st.subheader("Total Records Uploaded per File  ")
       fig=px.bar(data,
                  x="rows",
                  y="name"
         
       )
       st.plotly_chart(fig)
       st.subheader("Uploads By")
       fig1=px.scatter(data,
                      x="uploaded_by",
                      y="name"
        )
       st.plotly_chart(fig1)
       
       st.subheader("Data")
       st.dataframe(data)       
     except Exception:
          st.error("Database connection failed. Please try again later.")
#fuctioon to display the selected button      
def dataset_choice():
  default=st.session_state.get("Selected","All")
  if default== "All":
    display_cyber_incidents()
    display_it_tickets () 
    display_datasets_metadata()
  elif default=="Cyber Incidents Data ":
    display_cyber_incidents()
  elif default=="IT Tickets Data ":
    display_it_tickets()
  else:
    display_datasets_metadata()
#calling the function     
dataset_choice()
#Button to go to Dashboard
if st.button("Go To Dashboard",use_container_width=True) :
           st.switch_page("Pages/1_Dashboard.py")
