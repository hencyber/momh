import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DATA_PATH = "backend/data/aterbetalning/csn_aterbetalning.json"
STORE_PATH = "backend/data/aterbetalning/vector_store"


def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def chunk_documents(pages):
    """delar upp texterna i mindre bitar"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    
    chunks = []
    for page in pages:
        bits = splitter.split_text(page["content"])
        for bit in bits:
            chunks.append({
                "text": bit,
                "source": page["url"],
                "title": page["title"]
            })
    return chunks


def create_vector_store(chunks):
    """skapar FAISS vector store med HuggingFace embeddings"""
    # samma modell som Orhan använder
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    
    texts = [c["text"] for c in chunks]
    metadatas = [{"source": c["source"], "title": c["title"]} for c in chunks]
    
    vector_store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    vector_store.save_local(STORE_PATH)
    
    print(f"Vector store skapad med {len(chunks)} chunks")
    return vector_store


if __name__ == "__main__":
    pages = load_data()
    print(f"Laddat {len(pages)} sidor")
    
    chunks = chunk_documents(pages)
    print(f"{len(chunks)} chunks skapade")
    
    create_vector_store(chunks)
    print("Klart!")
