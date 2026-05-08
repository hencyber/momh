# Datapipeline för CSN Återbetalning (Henke)
# Skrapar CSN-sidor om återbetalning, chunkar och skapar vector store.
# Körs en gång för att förbereda data – se 'make setup-henke'.
#
# TODO (Henke): Lägg till dina CSN-URLs för återbetalning och implementera scraper.

import json

import requests
from bs4 import BeautifulSoup
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# TODO (Henke): Lägg till relevanta CSN-sidor för återbetalning
CSN_URLS = [
    # "https://www.csn.se/aterbetalning.html",
]

# Namn på embedding-modellen – multilingual för att hantera svenska frågor
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Sökväg där vector store sparas (relativt aterbetalning/-mappen)
VECTOR_STORE_PATH = "aterbetalning_vector_store"


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
    # Skapa en FAISS vector store från chunks och spara till disk
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    texts = [c["text"] for c in chunks]
    metadatas = [{"source": c["source"], "title": c["title"]} for c in chunks]
    vector_store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    vector_store.save_local(VECTOR_STORE_PATH)
    print(f"Vector store skapad med {len(chunks)} chunks")
    return vector_store


if __name__ == "__main__":
    pages = scrape_all()

    with open("aterbetalning_data.json", "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)

    print(f"\n{len(pages)} sidor sparade")
    chunks = chunk_documents(pages)
    print(f"{len(chunks)} chunks skapade")
    create_vector_store(chunks)
