"First run the following command in bash/terminal to install the required packages:"
"pip install -r requirements.txt"

# How to run the code
"""
Step 1: Run the FastAPI server -   python -m uvicorn chatbot_ui:app --reload
Step 2: 


"""

import chatbot
import navigation

def start_chat():
    print("Hi how can i help you become a superhuman race?")
  
    
    while True:
        print(" ")
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye', 'thank you']:
            print("Happy helping, Goodbye!")
            break
        
        if "navigation" in user_input.lower() or "website" in user_input.lower():
            print(f"Bot: {navigation.handle_navigation(user_input)}")
        else:
            print(f"Bot: {chatbot.handle_query(user_input)}")
    print("Type 'Thank you' to quit.")

# Start chatbot
if __name__ == "__main__":
    start_chat()
