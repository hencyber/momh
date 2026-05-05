from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import anthropic
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(__file__).parent.parent / ".env")

client = anthropic.Anthropic()

# Ladda vector store från disk
def load_vector_store():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    vector_store = FAISS.load_local(
        "csn_vector_store",
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vector_store

# Hitta relevanta chunks baserat på frågan
def retrieve_context(question: str, vector_store, k: int = 3) -> list:
    results = vector_store.similarity_search(question, k=k)
    return results

# Skicka fråga + kontext till Claude och få svar
def ask_claude(question: str, context_docs: list) -> dict:
    context = "\n\n".join([doc.page_content for doc in context_docs])
    sources = list(set([doc.metadata["source"] for doc in context_docs]))
    
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
                "content": f"""Kontext från CSN:
{context}

Fråga: {question}"""
            }
        ]
    )
    
    return {
        "answer": message.content[0].text,
        "sources": sources
    }
# Huvudfunktion som kopplar ihop allt
def answer_question(question: str) -> dict:
    vector_store = load_vector_store()
    context_docs = retrieve_context(question, vector_store)
    return ask_claude(question, context_docs)

if __name__ == "__main__":
    question = "Hur mycket studiemedel kan jag få?"
    print(f"Fråga: {question}\n")
    result = answer_question(question)
    print(f"Svar: {result['answer']}")
    print(f"\nKällor: {result['sources']}")