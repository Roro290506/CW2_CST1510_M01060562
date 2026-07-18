import smtplib
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#Function to send email when a user registers
def send_welcome_email(register_username,email):
    #sender email and password stored in secrets.toml
    sender_email = st.secrets["email"]["address"]
    sender_password = st.secrets["email"]["password"]
    #creation of container to build email's messages
    message=MIMEMultipart()
    #email message
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = "🎊Registration Successful!"
    body = f"""
    Hi {register_username},
    Thank you for registering to the Digital Forensics Website ! ...
    """
    #Conversion into text compatible with emails
    message.attach(MIMEText(body, "plain"))
    try:
        #establishes the port of communication for gmail
        service=smtplib.SMTP("smtp.gmail.com",587)
        #starts the secure communication
        service.starttls()
        #logs on the website gmail account
        service.login(sender_email,sender_password)
        #sending of the actual email
        service.sendmail(sender_email,email,message.as_string())
        #closing connection
        service.quit()
        return True
    except Exception:
        return False
#function to send password reset email
def send_reset_email(db_email,db_name,reset_link):
    #import password and email stored in secrets toml
    sender_email=st.secrets["email"]["address"]
    sender_password=st.secrets["email"]["password"]
    #creation of the email
    message=MIMEMultipart()
    message["From"]=sender_email
    message["To"]=db_email
    message["Subject"]="Reset Your Password"
    body=f"""
    Hi {db_name}
    You have requested for a password reset for your Data Forensics account with the username {db_name}.
    Click on the below link to reset your password.
    
    {reset_link}
    The link is only valid for the next 15 minutes.If you did not initiate the password reset ,ignore the email.
    
    Thank you
    Team IT Support
    """
    #converting message into text compartible to emails
    message.attach(MIMEText(body,"plain"))
    #establishing connection and sending of email
    try:
        service=smtplib.SMTP("smtp.gmail.com",587)
        service.starttls()
        service.login(sender_email,sender_password)
        service.sendmail(sender_email,db_email,message.as_string())
        service.quit()
        return True
    except Exception:
        return False
#function to send password update
def send_successpsw_update(email,username):
    #import sende email and password stored in secrets toml
    sender_email=st.secrets["email"]["address"]
    sender_password=st.secrets["email"]["password"]
    #Creation of message
    message=MIMEMultipart()
    message["From"]=sender_email
    message["To"]=email
    message["Subject"]="Password Update"
    body=f"""
    Hi {username}
    You've successfully updated your password for your Data Forensics account.
    
    Thank you
    Team IT Support
    """ 
    message.attach(MIMEText(body,"plain")) 
    #establishing connection and sending email
    try:
        service=smtplib.SMTP("smtp.gmail.com",587)
        service.starttls()
        service.login(sender_email,sender_password)
        service.sendmail(sender_email,email,message.as_string())
        service.quit()
        return True 
    except Exception :
        return False  
 #function to send email that acoount was deleted    
def send_delete_update(email,username):
    #importing senders email and password stored in secrets.toml
    sender_email=st.secrets["email"]["address"]
    sender_password=st.secrets["email"]["password"]
    #creation of email message
    message=MIMEMultipart()
    message["From"]=sender_email
    message["To"]=email
    message["Subject"]="Password Update"
    body=f"""
    Hi {username}
    You've successfully deleted your Data Forensics account.
     I hope you had a good experience  working with our website and we are open to reviews to be sent to this email about your experience.
     
    Team IT Support
    """ 
    message.attach(MIMEText(body,"plain")) 
    #sending of email and establishing connection
    try:
        service=smtplib.SMTP("smtp.gmail.com",587)
        service.starttls()
        service.login(sender_email,sender_password)
        service.sendmail(sender_email,email,message.as_string())
        service.quit()
        return True 
    except Exception :
        return False  
    
    
       