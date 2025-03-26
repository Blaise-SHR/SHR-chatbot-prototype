import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Gemini API Key
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
print("GOOGLE_API_KEY successfully loaded!") if GOOGLE_API_KEY else print("GOOGLE_API_KEY not found!")  
