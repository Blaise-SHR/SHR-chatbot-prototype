import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Fetch from environment variables

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing! Set it in Streamlit Secrets or config.py")

print("GOOGLE_API_KEY successfully loaded!") if GOOGLE_API_KEY else print("GOOGLE_API_KEY not found!")  
