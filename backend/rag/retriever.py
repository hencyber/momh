# RAG-retriever för CSN Studiestöd (Orhan)
# Hanterar inläsning av FAISS vector store, kontextsökning och Claude-anrop.
# answer_question() accepterar en redan-laddad vector store för bättre prestanda.

from pathlib import Path

import anthropic
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv(Path(__file__).parent.parent / ".env")

# Anthropic-klient för Claude-anrop
client = anthropic.Anthropic()

# Namn på embedding-modellen – multilingual för att hantera svenska frågor
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Sökväg till sparad FAISS vector store (relativt backend/-mappen)
VECTOR_STORE_PATH = "csn_vector_store"


def load_vector_store():
    # Ladda FAISS vector store från disk med rätt embedding-modell
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    # allow_dangerous_deserialization krävs av FAISS för pickle-baserad lagring.
    # Säkert här eftersom vi kontrollerar källan till index-filen.
    vector_store = FAISS.load_local(
        VECTOR_STORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vector_store


def retrieve_context(question: str, vector_store, k: int = 3) -> list:
    # Sök och returnera de k mest relevanta dokumentchunks för frågan
    results = vector_store.similarity_search(question, k=k)
    return results


# LLM-genererad kod – system-prompt och meddelandeformat
def ask_claude(question: str, context_docs: list) -> dict:
    # Bygg ihop kontext och unika källhänvisningar från hämtade chunks
    context = "\n\n".join([doc.page_content for doc in context_docs])
    sources = list(set([doc.metadata["source"] for doc in context_docs]))

    # Skicka fråga + kontext till Claude och returnera svar med källor
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="""Du är en kunnig och hjälpsam CSN-assistent som specialiserar sig på studiestöd, bidrag och lån.

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


if __name__ == "__main__":
    question = "Hur mycket studiemedel kan jag få?"
    print(f"Fråga: {question}\n")
    result = answer_question(question)
    print(f"Svar: {result['answer']}")
    print(f"\nKällor: {result['sources']}")