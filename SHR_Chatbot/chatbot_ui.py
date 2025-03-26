# FastAPI Backend for Chatbot UI
# pip install fastapi uvicorn pydantic
# Run this FastAPI backend with: `python -m uvicorn chatbot_ui:app --reload


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chatbot
import navigation

app = FastAPI()

class QueryRequest(BaseModel):
    user_input: str

@app.post("/chat")
def chat_response(request: QueryRequest):
    user_input = request.user_input.lower()
    
    if user_input in ['exit', 'quit', 'bye', 'goodbye', 'thank you']:
        return {"response": "Happy helping, Goodbye!"}
    
    if "navigation" in user_input or "website" in user_input:
        return {"response": navigation.handle_navigation(user_input)}
    else:
        return {"response": chatbot.handle_query(user_input)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

