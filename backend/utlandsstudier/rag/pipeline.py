# Datapipeline för CSN Utlandsstudier (Mona)
# Skrapar CSN-sidor om utlandsstudier och bygger ChromaDB vector store.
# Körs en gång för att förbereda data – se 'make setup-mona'.
#
# TODO (Mona): Lägg till dina CSN-URLs och implementera ChromaDB-skapandet.

import json

import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# TODO (Mona): Lägg till relevanta CSN-sidor för utlandsstudier
CSN_URLS = [
    # "https://www.csn.se/bidrag-och-lan/studera-utomlands.html",
]

# Sökväg där ChromaDB-databasen sparas (gitignorerad)
CHROMA_DB_PATH = "../data/chroma_utlandsstudier"

# Namn på embedding-modellen – multilingual för att hantera svenska frågor
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def scrape_page(url: str) -> dict:
    # Hämta och extrahera text från en CSN-sida
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "No title"
    paragraphs = soup.find_all("p")
    content = " ".join([p.get_text(strip=True) for p in paragraphs])
    return {"url": url, "title": title, "content": content}


def scrape_all() -> list:
    # Skrapa alla sidor och samla resultaten i en lista
    pages = []
    for url in CSN_URLS:
        print(f"Skrapar: {url}")
        page = scrape_page(url)
        pages.append(page)
        print(f"  → {page['title']} ({len(page['content'])} tecken)")
    return pages


def chunk_documents(pages: list) -> list:
    # Dela upp varje sidas innehåll i mindre bitar med överlappning
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = []
    for page in pages:
        bits = splitter.split_text(page["content"])
        for bit in bits:
            chunks.append({"text": bit, "source": page["url"], "title": page["title"]})
    return chunks


def create_vector_store(chunks: list):
    # TODO (Mona): Implementera ChromaDB-skapandet här
    # Exempelstruktur:
    #   import chromadb
    #   from langchain_community.vectorstores import Chroma
    #   from langchain_huggingface import HuggingFaceEmbeddings
    #   embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    #   vector_store = Chroma.from_texts(
    #       texts=[c["text"] for c in chunks],
    #       embedding=embeddings,
    #       metadatas=[{"source": c["source"], "title": c["title"]} for c in chunks],
    #       persist_directory=CHROMA_DB_PATH
    #   )
    #   print(f"ChromaDB skapad med {len(chunks)} chunks")
    #   return vector_store
    raise NotImplementedError("create_vector_store() är inte implementerad för ChromaDB")


if __name__ == "__main__":
    pages = scrape_all()

    with open("utlandsstudier_data.json", "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)

    print(f"\n{len(pages)} sidor sparade")
    chunks = chunk_documents(pages)
    print(f"{len(chunks)} chunks skapade")
    create_vector_store(chunks)
