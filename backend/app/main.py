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


# Extract answer and sources from response
def extract_answer_and_sources(full_response: str):
    if "KÄLLA:" in full_response:
        parts = full_response.split("KÄLLA:", 1)  # safer split
        answer_text = parts[0].strip()
        source_text = parts[1].strip()
        return answer_text, [source_text]

    # fallback if no source found
    print("⚠️ No source from RAG")
    return full_response, []


# Endpoint /chat
@app.post("/chat", response_model=ChatResponse)
def chat_utlandsstudier(request: ChatRequest):
    """Receives a question and returns answer + sources"""

    if chain is None:
        raise HTTPException(
            status_code=500,
            detail="RAG-chain is not loaded"
        )

    try:
        # Send question to RAG-chain
        full_response = chain.invoke(request.question)

        # Extract answer and sources
        answer_text, sources_list = extract_answer_and_sources(full_response)

        # Return result
        return {
            "answer": answer_text,
            "sources": sources_list
        }

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
