from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

# lägg till parent path så vi kan importera rag
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from rag import ask

app = FastAPI(title="CSN Återbetalning API")


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    """tar emot en fråga och returnerar svar från RAG"""
    try:
        answer, sources = ask(request.question)
        return ChatResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
