# Huvudfil för CSN Utlandsstudier-backend (Mona)
# FastAPI-applikation som exponerar POST /chat för utlandsstudierfrågor.
# Port: 8003 (se API_CONTRACT.md)
# Använder ChromaDB som vector store (till skillnad från Orhan/Henke som kör FAISS).
#
# VIKTIGT: ChromaDB-data är gitignorerad (backend/data/).
# Kör 'make setup-mona' för att skrapa och bygga vector store innan första start.

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

# TODO (Mona): Avkommentera när retriever är klar
# from rag.retriever import answer_question, load_vector_store

# Global referens till vector store – laddas en gång vid startup
_vector_store = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO (Mona): Ladda ChromaDB vector store vid startup
    # global _vector_store
    # _vector_store = load_vector_store()
    yield


app = FastAPI(title="CSN Utlandsstudier API", lifespan=lifespan)


# Request- och response-modeller enligt API-kontraktet (API_CONTRACT.md)
class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # TODO (Mona): Ersätt med riktig RAG-pipeline (ChromaDB)
    try:
        # result = answer_question(request.question, _vector_store)
        # return ChatResponse(answer=result["answer"], sources=result["sources"])
        raise NotImplementedError(
            "Monas RAG-pipeline är inte integrerad än. "
            "Kör 'make setup-mona' för att bygga ChromaDB vector store."
        )
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Något gick fel: {str(e)}")


@app.get("/health")
def health():
    # Hälsocheck för Docker/Kubernetes och lastbalanserare
    return {"status": "ok"}


@app.get("/")
def index():
    # Servera HTML-gränssnittet om det finns
    return FileResponse("templates/index.html")
