from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

STORE_PATH = os.path.join(os.path.dirname(__file__), "../../data/aterbetalning/vector_store")

# ladda vector store
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
vector_store = FAISS.load_local(STORE_PATH, embeddings, allow_dangerous_deserialization=True)

# openrouter klient
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def search(query, k=3):
    """söker i vector store efter relevanta dokument"""
    results = vector_store.similarity_search(query, k=k)
    return results


def ask(question):
    """tar emot en fråga och returnerar svar + källor"""
    # hämta relevanta dokument
    docs = search(question)
    
    # bygg context från dokumenten
    context = ""
    sources = []
    for doc in docs:
        context += doc.page_content + "\n\n"
        source = doc.metadata.get("source", "")
        if source and source not in sources:
            sources.append(source)
    
    # skicka till LLM
    response = client.chat.completions.create(
        model="nvidia/nemotron-3-nano-30b-a3b:free",
        messages=[
            {
                "role": "system",
                "content": (
                    "Du är en hjälpsam assistent som svarar på frågor om återbetalning av studielån från CSN. "
                    "Svara baserat på kontexten. Om du inte hittar svaret, hänvisa till csn.se. "
                    "Svara på svenska, kortfattat och tydligt."
                )
            },
            {
                "role": "user",
                "content": f"Kontext:\n{context}\n\nFråga: {question}"
            }
        ],
    )
    
    answer = response.choices[0].message.content
    return answer, sources


if __name__ == "__main__":
    # snabbtest
    svar, källor = ask("Hur mycket ska jag betala på mitt lån?")
    print(f"Svar: {svar}")
    print(f"Källor: {källor}")
