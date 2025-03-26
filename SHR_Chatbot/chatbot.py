import os
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
import config
from config import GOOGLE_API_KEY  # Import API key from config.py

# Load documents
faq_loader = TextLoader("knowledge-base/shr-faq.txt", encoding="utf-8")
navigation_loader = TextLoader("knowledge-base/platform-navigation-guide.txt", encoding="utf-8")

faq_documents = faq_loader.load()
navigation_documents = navigation_loader.load()
all_documents = faq_documents + navigation_documents

# Ensure API key is set
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set. Check your config.py or .env file.") 

# Create embeddings and vector store
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GOOGLE_API_KEY
)

vector_store = FAISS.from_documents(all_documents, embeddings)

# Initialize Google Gemini Model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)

# Custom prompt
prompt_template = """
You are a knowledgeable and efficient AI assistant trained on the SHR FAQ and platform navigation guide.
Your role is to provide accurate, concise, and user-friendly responses based on the information in these documents.

- If the question relates to **platform navigation**, offer clear step-by-step guidance along with the relevant link.
- If the question pertains to **general queries or FAQs**, provide precise, well-structured answers.
- If the question is **ambiguous or unclear**, ask for clarification to provide the best possible response.
- If the requested information is unavailable, politely acknowledge it rather than guessing
  and advise the client to seek help from the respective account manager.
- Along with answering the user query, provide the module it belongs to.

Now, answer the following question:

{question}
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["question"])

# Conversational Retrieval Chain with the correct retriever
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vector_store.as_retriever(),
    return_source_documents=True  # Ensures sources are returned for reference
)

# Function to handle user queries
chat_history = []  # Initialize chat history

def handle_query(query):
    global chat_history  # Maintain conversation history

    # Debugging print statement
    #print("DEBUG chat_history:", chat_history)

    # Ensure chat_history contains valid tuples
    processed_history = [(q, a.get("answer", a) if isinstance(a, dict) else a) for q, a in chat_history]

    # Invoke the QA chain
    response = qa_chain.invoke({
        "question": query,
        "chat_history": processed_history  
    })

    # Extract just the answer
    answer = response.get("answer", "Sorry, I couldn't find an answer to that.")

    # Store the latest query-response pair in history
    chat_history.append((query, answer))


    return answer  # Return only the answer
    print(" ")

    # Append conversation with only question & string response to avoid dictionary issue
    chat_history.append((query, response["answer"]))  
    return response["answer"]  # Return only the relevant answer
