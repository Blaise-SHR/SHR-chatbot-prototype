# Streamlit UI for Chatbot
# pip install streamlit requests
# python -m streamlit run streamlit_chatbot_ui.py

import streamlit as st 
import requests

st.title("SHR Support Chatbot")

user_input = st.text_input("You:", "")

if user_input:
    response = requests.post("http://127.0.0.1:8000/chat", json={"user_input": user_input})
    if response.status_code == 200:
        bot_response = response.json()["response"]
        st.write(f"**Bot:** {bot_response}")
    else:
        st.write("Error: Could not get a response from the chatbot.")
