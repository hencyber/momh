# Huvudfil för CSN Studiestöd-backend (Orhan)
# FastAPI-applikation som exponerar POST /chat för studiestödsfrågor.
# Startar FAISS vector store vid uppstart för att undvika omladdning vid varje anrop.
# Port: 8001 (se API_CONTRACT.md)

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from rag.retriever import answer_question, load_vector_store

# Global referens till vector store – laddas en gång vid startup för bättre prestanda
_vector_store = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ladda FAISS vector store en gång när applikationen startar
    global _vector_store
    _vector_store = load_vector_store()
    yield


app = FastAPI(title="CSN Studiestöd API", lifespan=lifespan)


# Request- och response-modeller enligt API-kontraktet (API_CONTRACT.md)
class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Skicka frågan till RAG-pipeline med förladdad vector store
    try:
        result = answer_question(request.question, _vector_store)
        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Något gick fel: {str(e)}")


@app.get("/health")
def health():
    # Hälsocheck för Docker/Kubernetes och lastbalanserare
    return {"status": "ok"}


@app.get("/")
def index():
    # Servera HTML-gränssnittet från templates/
    return FileResponse("templates/index.html")