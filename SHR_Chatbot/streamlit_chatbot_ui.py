import os
os.system("pip install -r requirements.txt")
import streamlit as st
from chatbot import handle_query  # Import the chatbot function

st.title("SHR Support Chatbot")
st.write("Hello I'm Ray!")
st.write("How can I help you become a SuperHuman today?")

#Input field for user to type in
user_input = st.text_input("You:", "", placeholder="Type 'thank you' to exit")

if user_input:
    bot_response = handle_query(user_input)  # Call the chatbot function directly
    st.write(f"**Ray:** {bot_response}")
