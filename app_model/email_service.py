import smtplib
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Home import register_username,email
def send_welcome_email():
    sender_email = st.secrets["email"]["address"]
    sender_password = st.secrets["email"]["password"]
    message=MIMEMultipart
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = "🎊Registration Successful!"
    body = f"""
    Hi {register_username},
    Thank you for registering! ...
    """
    message.attach(MIMEText(body, "plain"))
    try:
        service=smtplib.SMTP("smtp.gmail.com",587)
        service.starttls
        service.login(sender_email,sender_password)
        service.sendmail(email,register_username,message.as_string())
        service.quit
        return True
    except:
        return False
    
    
    