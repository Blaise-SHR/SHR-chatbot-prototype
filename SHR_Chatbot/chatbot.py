import os
import requests
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
import config
from config import GOOGLE_API_KEY  # Import API key from config.py

# URLs for document sources
FAQ_URL = "https://github.com/Blaise-SHR/SHR-chatbot-prototype/blob/main/SHR_Chatbot/knowledge-base/shr-faq.txt"
NAVIGATION_URL = "https://github.com/Blaise-SHR/SHR-chatbot-prototype/blob/main/SHR_Chatbot/knowledge-base/platform-navigation-guide.txt"
# Function to fetch content from a URL
def fetch_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error if the request failed
        return response.text
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching {url}: {e}")

# Load documents from URLs
faq_text = fetch_text_from_url(FAQ_URL)
navigation_text = fetch_text_from_url(NAVIGATION_URL)

# Convert text into LangChain documents
from langchain.schema import Document
faq_documents = [Document(page_content=faq_text)]
navigation_documents = [Document(page_content=navigation_text)]
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
Prompt:
-------
Context:
Your name is Ray. You are a very intelligent chatbot for the SuperHuman Race company's website. 

Story of SuperHuman Race:
In 2016, we started the journey of building a platform that could measure 'good', just like profitability is measured...
(Full company story remains unchanged)

Instructions:
------------
Your role is to solve user queries and navigation requests.
Explain it as if they are five-year-old users. Simplify as much as possible.

- If the question relates to **platform navigation**, offer clear step-by-step guidance along with the relevant link.
- If the question pertains to **general queries or FAQs**, provide precise, well-structured answers.
- If the question is **ambiguous or unclear**, ask for clarification.
- If the requested information is unavailable, politely acknowledge it rather than guessing.
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
