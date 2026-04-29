import requests
import json
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
# Lista över CSN-sidor att skrapa
CSN_URLS = [
    "https://www.csn.se/bidrag-och-lan.html",
    "https://www.csn.se/bidrag-och-lan/studiestod.html",
    "https://www.csn.se/bidrag-och-lan/omstallningsstudiestod.html",
    "https://www.csn.se/bidrag-och-lan/for-din-situation.html",
    "https://www.csn.se/bidrag-och-lan/tillagg-till-studiestodet.html",
    "https://www.csn.se/bidrag-och-lan/tuff-ersattning.html",
]
# Skrapa varje sida, extrahera titel och textinnehåll, och spara i en lista av dicts
def scrape_page(url: str) -> dict:
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    # Försök hitta en titel i h1-taggen, annars använd "No title"
    title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "No title"
    # Extrahera text från alla p-taggar och sammanfoga till en enda sträng
    paragraphs = soup.find_all("p")
    content = " ".join([p.get_text(strip=True) for p in paragraphs])
    
    return {
        "url": url,
        "title": title,
        "content": content
    }
# Skrapa alla sidor och samla resultaten i en lista
def scrape_all() -> list:
    pages = []
    for url in CSN_URLS:
        print(f"Skrapar: {url}")
        page = scrape_page(url)
        pages.append(page)
        print(f"  → {page['title']} ({len(page['content'])} tecken)")
    return pages
# Dela upp varje sidas innehåll i mindre bitar (chunks) med överlappning, och behåll metadata som källa och titel
def chunk_documents(pages: list) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    # Skapa en lista av chunks där varje chunk är en dict med text, källa (URL) och titel
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
# Skapa en vektorbutik (vector store) från listan tillsammans med metadata
def create_vector_store(chunks: list):
    # Laddar embedding-modell som förstår svenska
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    
    texts = [c["text"] for c in chunks]
    metadatas = [{"source": c["source"], "title": c["title"]} for c in chunks]
    
    vector_store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    vector_store.save_local("csn_vector_store")
    
    print(f"Vector store skapad med {len(chunks)} chunks")
    return vector_store
# Huvudkörning: skrapa sidor, chunkar och embeddar
if __name__ == "__main__":
    pages = scrape_all()
    
    with open("csn_data.json", "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)
    
    print(f"\n{len(pages)} sidor sparade till csn_data.json")
    
    print("\n=== CHUNKAR OCH EMBEDDAR ===")
    chunks = chunk_documents(pages)
    print(f"{len(chunks)} chunks skapade")
    
    create_vector_store(chunks)