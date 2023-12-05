# Author: chatgpt
# date: 05.12.2023

import streamlit as st
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Streamlit UI
st.title("Secret Santa App")

with st.form("participant_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    submit_button = st.form_submit_button("Submit")

if 'participants' not in st.session_state:
    st.session_state['participants'] = []

if submit_button:
    st.session_state['participants'].append({'name': name, 'email': email})

# Display participants
st.write("Participants:")
for participant in st.session_state['participants']:
    st.write(participant['name'])

# Secret Santa Logic
def assign_secret_santa(participants):
    shuffled = participants[:]
    random.shuffle(shuffled)
    for i in range(len(shuffled)):
        receiver_index = (i + 1) % len(shuffled)
        shuffled[i]['receiver'] = shuffled[receiver_index]['name']
    return shuffled

# Email Sending Function
def send_emails(assigned):
    # Configure SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(os.getenv('EMAIL'), os.getenv('PASSWORD'))
    
    for participant in assigned:
        msg = MIMEMultipart()
        msg['From'] = os.getenv('EMAIL')
        msg['To'] = participant['email']
        msg['Subject'] = "Secret Santa Assignment"
        body = f"You are the Secret Santa for {participant['receiver']}!"
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        server.sendmail(os.getenv('EMAIL'), participant['email'], text)
    server.quit()

# Button to Trigger Assignment
if st.button("Assign Secret Santas"):
    assigned = assign_secret_santa(st.session_state['participants'])
    send_emails(assigned)
    st.session_state['participants'].clear()  # Clearing participants data
    st.success("Secret Santa assigned and emails sent!")

# Clear Participants List
if st.button("Clear Participants"):
    st.session_state['participants'].clear()
    st.success("Participants list cleared!")

