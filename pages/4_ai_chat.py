
import streamlit as st 
import time
import pandas as pd
from groq import Groq
from app_model.logic.ai_prompt import insert_prompt
from app_model.db import get_connection

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in to access your profile.")
    if st.button("Go To Log In"):
        st.switch_page('Home.py')
    st.stop()

client = Groq(api_key=st.secrets["api"]["key"])
st.title("🤖 Chat with GPT")

#Informing the LLM what the database looks like 
database_schema=""" 
You have read only access to the SQLite Database with the exact tables and columns:

TABLE : cyber_incidents
-incident_id(INTEGER,Primary key): Unique identifier for the incident eg 1000.
-timestamp(DATETIME): The date and time of incident eg 2024-03-28 20:00:00.000000.
-severity(TEXT): Severity Levels -values are exactly: Low,Medium,High or Critical.
-category(TEXT): Type of Incident eg Malware,Ransomware ,Phishing.
-status(TEXT): Current status -values are exactly:Open,Resolved,In Progress,Closed.
-description(TEXT): Incident description eg Incident 76 description.

TABLE : it_tickets
-ticket_id(INTEGER,Primary key): Unique Identifier for it ticket eg 2000.
-priority(TEXT): Level of priority -values are exactly:Low,Medium,High.
-description(TEXT):Ticket problem description eg Ticket 0 problem description.
-status(TEXT): Current status -values are exactly:Open,Resolved,In Progress,Waiting for User.
-assigned_to(TEXT): Group assigned the ticket eg IT_Support_C
-created_at(DATETIME): the date and time of ticket creation eg 2024-08-06 07:00:00
-resolution_time_hours(INTEGER): Time taken for resolution eg 37.

TABLE : datasets_metadata
-dataset_id(INTEGER): Unique Identifier for dataset eg 1
-name(TEXT): Name of Dataset eg Customer_Churn
-rows(INTEGER): Number of records recorded on dataset eg 5000
-columns(INTEGER): segments being monitored per dataset eg 15
-uploaded_by(TEXT): Person who uploaded it eg data_scientist
-upload_date(DATE): Date of upload eg 2024-01-15

CRITICAL INSTRUCTION: Return ONLY the plain executable SQL query string. Do not include markdown code fences (like ```sql), do not include explanations, and do not include backticks.
"""
def generate_sql(prompt):
    #Instruction on generating sql
    system_instruction=(
        f"{database_schema}"
        """Your Job:
           1.check if the user's question requires a database query
           2.If yes  your sole purpose is to convert the user's question into a functionally correct SQLite query
           3.If no and the question is conceptual then  respond with NO SQL NEEDED
           Your Rules:
           -Only return sql query or NO SQL NEEDED
           -Do not include explanations
           -Only use the tables and columns provided in database schema
        """
                        )
    #User query and query generation
    sql_response = client.chat.completions.create(
        model    = "openai/gpt-oss-120b",
        messages = [
            {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Provide the raw SQL query for: {prompt}"}
        ],
        stream =False
    )
    #generated query response
    generated_sql = sql_response.choices[0].message.content.strip()
    #the output if question is not in the database
    if "NO SQL NEEDED" in generated_sql.upper():
        return client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system",
                 "content": """Act as a triple expert as an IT operations lead, Senior Cybersecurity Analyst and Data Science Expert
                 CRITICAL SCOPE LIMITATION: You are permitted to answer only questions related to
                 -Terms related to Cybersecurity,Data Science and IT Operations
                 -Analyse incidents using MITRE ATT&CK and CVE references.
                 -Provide structured responses: Root Cause, Immediate Actions, Prevention Measures, Risk Level.
                 -Help with dataset analysis, choosing visualisation types, statistical methods and machine learning and suggest concrete next steps."
                 -Prioritise support tickets by impact and urgency, suggest troubleshooting steps and provide infrastructure best practices
                 """
                 },
                {"role": "user", "content": prompt}
            ],
            stream=True 
        )
    #else it reads from database
    conn=get_connection()
    try:
      df=pd.read_sql_query(generated_sql,conn)
      raw_data=df.to_string()
    except Exception :
        st.error("Error")
        raw_data="No data found due to an error"
    finally:
        conn.close()
    
   #production of  final response
    final_response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are an analytical system assistant. Translate raw database table data into a polished, natural language answer for the user."},
                {"role": "user", "content": f"User Question: {prompt}\n\nExecuted SQL Query used: {generated_sql}\n\nReturned Data Table:\n{raw_data}"}
            ],
            stream=True
        )
    return final_response
    


# Initialise message history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for msg in st.session_state.messages:
    if msg["role"] != "system":          # Don't show system prompt
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# New user input
if prompt := st.chat_input(f"{st.session_state["username"]} Ask a question about cyber incidents,IT tickets and datasets metadata ?"):
    start_time=time.time()
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})    

    # Get AI response
    response = generate_sql(prompt)
    full_reply = ""
    placeholder = st.empty()      
    # Iterate over streamed chunks
    for chunk in response:        
        delta = chunk.choices[0].delta.content
        if delta:
            full_reply  += delta
            placeholder.write(full_reply + "▌")   
    # Final output without cursor
    placeholder.write(full_reply) 
    endtime=time.time()
    response_time=int((endtime-start_time)*1000)
    insert_prompt(st.session_state["user_id"],prompt,full_reply,response_time)
    # Add complete reply to session state
    st.session_state.messages.append({"role": "assistant", "content": full_reply})
