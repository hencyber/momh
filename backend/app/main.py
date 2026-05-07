### API adapted to our structure

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Importing RAG-function
from backend.app.utlandsstudier.rag import setup_rag_chain

# Creating API application
app = FastAPI(title="Utlandsstudier API")


# Load RAG-chain
def load_chain():
    """Loads RAG-chain, returns None if it fails"""
    try:
        return setup_rag_chain()
    except Exception as error:
        print("Error: failed loading RAG-chain:", error)
        return None


chain = load_chain()


# Define request (input)
class ChatRequest(BaseModel):
    question: str


# Define response (output)
class ChatResponse(BaseModel):
    answer: str
    sources: List[str]


# Removed section "Extract answer and sources from response REMOVED!

# Added healthcheck 
@app.get("/health")
def health():
    return {"status": "ok"}

# Endpoint /chat
@app.post("/chat", response_model=ChatResponse)
def chat_utlandsstudier(request: ChatRequest):
    """Receives a question and returns answer + sources"""

    if chain is None:
        raise HTTPException(
            status_code=500,
            detail="RAG-chain is not loaded"
        )
# REMOVED : Invoke which returned string , parsing logic 
    try:
        response = chain(request.question) # Added structured rag function

        return response # Added return structured response directly

    except Exception as error:
        print("Error with API call:", error)

        raise HTTPException(
            status_code=500,
            detail="Internal issue occurred"
        )


# Start server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8003
    )