import chatbot  # Import the chatbot function

def handle_navigation(query):
    # Basic logic to identify navigation queries
    if "where" in query.lower() or "how to" in query.lower():
        return "You can navigate using the website's top menu. Let me know if you need specific guidance."
    else:
        return chatbot.handle_query(query)  # Default to FAQ response
