A SECURE MULTI-DOMAIN INTELLIGENCE PLATFORM

##Introduction
A high performance Python and Streamlit based intelligence platform designed for the visualization and analysis of cyber incident data, IT tickets and dataset metadata. This platform leverages contextualized Large Language Models (LLMs) to provide actionable insights into complex security datasets.

##Features and Functionality
-Secure Multi User Access:Built in aunthentication to ensure role based acess control(RBAC) and data privacy.
-Unified Forensics Dashboard:Visualize cyber incidents,IT tickets and datsets metadatain one interface.
-Interactive Analytic: High visualization to identify trends and anomalies in data .
-AI Driven:Contextualized LLM integration to generate sql and return data and also provide insight to related topic to cyber security,it operation and data science .
-Secure Account Recovery-Features an automated email based recovery workflow using stmplib and tokenization ensuring authorized personnel mantain seamless access to their accounts.

##Security Implementation(Defense in Depth)
-Registration Security:User inputs validated via 1.Regex to ensure robust password 2.Bcrypt password hashing
-Authentication Integrity:Utilization of bcrypt.checkpw for secure credential verification,ensuring hashes are resistant to brute force attacks
-Access Control:The system enforces strict RBAC to ensure that log details,ai prompts details and user details except hash are accessible to admin.The admin role is hardcoded in the database.
-Account Recovery:Secure automated email based recovery implemented using smtplib and stramlit tokenization.

##Technical Stack
-Frontend: Streamlit and Plotly
-Data Processing:Pandas
-Intelligence Engine: Groq AI
-Authentication & Security: bcrypt and SQLite
-Communication: smtplip
-Database Engine: SQLite

##Architecture
CW2_CST1510_M01060562/
├── .streamlit/             # Configuration and secrets
├── app_model/              # Core application modellayer
│   ├── logic/              #Conversion of database tables into dataframes
│   │   ├── ai_prompt.py    
│   │   ├── cyber_incidents.py
│   │   ├── it_tickets.py
│   │   ├── logs.py
│   │   └── metadatas.py
│   ├── db.py               # Database connections
│   ├── email_service.py    # Communication services
│   ├── hashing.py          # Password security (bcrypt)
│   └── schema.py           # Database schema
├── DATA/                   # Datasets and SQLite db
├── pages/                  # Streamlit dashboard pages
├── Home.py                 # Platform entry point
└── main.py                 # Main controller

##Database Schema & Data Structure
-The platform utilizes a local SQLite database ("DATA/project_data.db").
The core tables are:
|Table Name |Description  |Key Fields
|ai_prompt  |Stores all the ai prompts and responses|prompt_id,user_id,time,prompt,response,response time
|cyber_incidents  |Store all cyber incidents data to be displayed  |incident id,timestamp,severity,category,status,description
|datasets_metadata  |Store all datasets metadata to be displayed  |dataset_id,name,rows,columns,uploaded_by,upload_date
|it_tickets   |Stores all it tickets information to be displayed   |ticket_id,priority,description,status,assigned_to,created_at,resolution
|logs   |Stores the timestamps for when the user logged in and out   |log_id,user_id,login_time,logout_time
|password_reset  |Stores token information for password reset   |id,email,token,time_created,expires_at
|users   |Store creadentials for the website users  |id,email,username,password_hash,role

##Installation and Setup 
-Prerequisites
Python 3.10 or higher
An API Key from Groq Cloud
-Clone the Repository 
Bash
git clone https://github.com/Roro290506/CW2_CST1510_M01060562
-Install Depedencies
pip install -r requirements.txt
-Configure Sensetive Credentials
.streamlit/secrets.toml
#SMTP Configuration
[email]
address = ""
password = ""
#Groq AI Configuration
[api]
key=""
-User Role
Hardcore the admin in the database
-Launch the website
python -m streamlit run Home.py


##Author
Ropafadzo Chidiya
Bsc(Hons) Cybersecurity and Digital Forensics
Middlesex University Mauritius

##License
This project was developed for academic coursework purposes.