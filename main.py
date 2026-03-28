from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest
from chat_engine import get_response
from crisis import contains_crisis_keywords, SAFETY_MESSAGE
from logger import log_chat

app = FastAPI()

# Enable CORS (for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Mental Health Chatbot Running 🚀"}

@app.post("/chat")
def chat(request: ChatRequest):
    session_id = request.session_id
    user_query = request.query

    # Crisis check
    if contains_crisis_keywords(user_query):
        log_chat(session_id, user_query, SAFETY_MESSAGE, True)
        return {"response": SAFETY_MESSAGE}

    # Normal chatbot response
    response = get_response(session_id, user_query)
    log_chat(session_id, user_query, response, False)

    return {"response": response}
  from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str
    query: str
  # Simple memory chatbot (no API needed)

session_memory = {}

def get_response(session_id: str, user_query: str) -> str:
    if session_id not in session_memory:
        session_memory[session_id] = []

    session_memory[session_id].append(user_query.lower())

    # Basic logic
    if "sad" in user_query.lower():
        return "I'm really sorry you're feeling sad. I'm here to listen 💙"
    elif "happy" in user_query.lower():
        return "That's great to hear! 😊"
    else:
        return "Thank you for sharing. Tell me more."
      CRISIS_KEYWORDS = [
    "suicide", "kill myself", "want to die",
    "hopeless", "worthless", "end my life"
]

SAFETY_MESSAGE = (
    "I'm really sorry you're feeling this way.\n"
    "You are not alone. Please reach out to someone.\n\n"
    "📞 India Helpline: 9152987821\n"
    "📞 USA: 988\n"
    "You matter 💙"
)

def contains_crisis_keywords(text: str) -> bool:
    text = text.lower()
    return any(word in text for word in CRISIS_KEYWORDS)
import csv
import os
from datetime import datetime

def log_chat(session_id, query, response, is_crisis):
    file = "chat_log.csv"
    exists = os.path.isfile(file)

    with open(file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow(["time", "session", "query", "response", "crisis"])

        writer.writerow([
            datetime.now(),
            session_id,
            query,
            response,
            is_crisis
        ])
        pip install fastapi uvicorn python-dotenv langchain openai
        uvicorn main:app --reload
      
