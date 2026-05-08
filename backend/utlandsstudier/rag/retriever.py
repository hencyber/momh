# RAG-retriever för CSN Utlandsstudier (Mona)
# Hanterar inläsning av ChromaDB vector store, kontextsökning och Claude-anrop.
# Samma mönster som Orhans retriever men med ChromaDB istället för FAISS.
#
# VIKTIGT: Kör 'make setup-mona' för att bygga ChromaDB-databasen innan start.
# Data lagras i backend/data/ som är gitignorerad.
#
# TODO (Mona): Implementera load_vector_store() med ditt ChromaDB-klientanrop.

from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

# Anthropic-klient för Claude-anrop
client = anthropic.Anthropic()

# Sökväg till ChromaDB-databasen (gitignorerad, måste byggas lokalt)
CHROMA_DB_PATH = "../data/chroma_utlandsstudier"

# Namn på embedding-modellen – multilingual för att hantera svenska frågor
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def load_vector_store():
    # TODO (Mona): Lägg till ChromaDB-import och implementera vector store-laddning
    # Exempelstruktur:
    #   import chromadb
    #   from langchain_community.vectorstores import Chroma
    #   from langchain_huggingface import HuggingFaceEmbeddings
    #   embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    #   client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    #   return Chroma(client=client, embedding_function=embeddings)
    raise NotImplementedError("load_vector_store() är inte implementerad för Monas ChromaDB")


def retrieve_context(question: str, vector_store, k: int = 3) -> list:
    # Sök och returnera de k mest relevanta dokumentchunks för frågan
    results = vector_store.similarity_search(question, k=k)
    return results


# LLM-genererad kod – system-prompt och meddelandeformat
def ask_claude(question: str, context_docs: list) -> dict:
    # Bygg ihop kontext och unika källhänvisningar från hämtade chunks
    context = "\n\n".join([doc.page_content for doc in context_docs])
    sources = list(set([doc.metadata["source"] for doc in context_docs]))

    # TODO (Mona): Anpassa system-prompten för utlandsstudierfrågor
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="""Du är en kunnig och hjälpsam CSN-assistent som specialiserar sig på utlandsstudier och studier utomlands.

Ditt uppdrag:
- Svara alltid på svenska
- Basera dina svar ENDAST på den information som ges i kontexten
- Om frågan är vag, ställ en följdfråga för att förstå situationen bättre
- Ge konkreta och specifika svar — undvik att säga "kontakta CSN" om svaret finns i kontexten
- Om informationen verkligen saknas i kontexten, var ärlig om det men förklara vad du vet
- Strukturera längre svar med punktlistor för tydlighet
- Håll en vänlig och professionell ton""",
        messages=[
            {
                "role": "user",
                "content": f"Kontext från CSN:\n{context}\n\nFråga: {question}"
            }
        ]
    )

    return {
        "answer": message.content[0].text,
        "sources": sources
    }


def answer_question(question: str, vector_store=None) -> dict:
    # Huvudfunktion: ladda vector store om ingen skickats med, hämta kontext och svara
    if vector_store is None:
        vector_store = load_vector_store()
    context_docs = retrieve_context(question, vector_store)
    return ask_claude(question, context_docs)
