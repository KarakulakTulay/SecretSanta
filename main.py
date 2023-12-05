# Author: chatgpt
# date: 05.12.2023

import streamlit as st
import random

# Streamlit UI
st.title("🎄 Simple Secret Santa App 🎄")

with st.form("participant_form"):
    name = st.text_input("Name")
    submit_button = st.form_submit_button("Submit")

if 'participants' not in st.session_state:
    st.session_state['participants'] = []

if submit_button and name:
    st.session_state['participants'].append(name)

# Display participants
st.write("Participants:")
for participant in st.session_state['participants']:
    st.write(participant)

# Secret Santa Logic
def assign_secret_santa(participants):
    shuffled = participants[:]
    random.shuffle(shuffled)
    assignments = {}
    for i in range(len(shuffled)):
        receiver_index = (i + 1) % len(shuffled)
        assignments[shuffled[i]] = shuffled[receiver_index]
    return assignments

# Button to Trigger Assignment
if st.button("Assign Secret Santas"):
    if len(st.session_state['participants']) < 2:
        st.error("Please add at least two participants.")
    else:
        assigned = assign_secret_santa(st.session_state['participants'])
        st.subheader("Secret Santa Assignments:")
        for giver, receiver in assigned.items():
            st.write(f"{giver} 🎁 → {receiver}")

# Clear Participants List
if st.button("Clear Participants"):
    st.session_state['participants'].clear()
    st.success("Participants list cleared!")

