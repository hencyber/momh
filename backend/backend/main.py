from fastapi import FastAPI
from pydantic import BaseModel
from rag.retriever import answer_question

app = FastAPI()

# Definiera request-formatet
class ChatRequest(BaseModel):
    question: str

# Definiera response-formatet
class ChatResponse(BaseModel):
    answer: str
    sources: list

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = answer_question(request.question)
    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"]
    )

@app.get("/health")
def health():
    return {"status": "ok"}