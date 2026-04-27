import requests
from bs4 import BeautifulSoup
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Sidor vi får skrapa enligt robots.txt
CSN_URLS = [
    "https://www.csn.se/bidrag-och-lan.html",
    "https://www.csn.se/bidrag-och-lan/studiestod.html",
    "https://www.csn.se/bidrag-och-lan/omstallningsstudiestod.html",
    "https://www.csn.se/bidrag-och-lan/for-din-situation.html",
    "https://www.csn.se/bidrag-och-lan/tillagg-till-studiestodet.html",
    "https://www.csn.se/bidrag-och-lan/tuff-ersattning.html",
]

def scrape_page(url: str) -> dict:
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    
    title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "No title"
    
    paragraphs = soup.find_all("p")
    content = " ".join([p.get_text(strip=True) for p in paragraphs])
    
    return {
        "url": url,
        "title": title,
        "content": content
    }

def scrape_all() -> list:
    pages = []
    for url in CSN_URLS:
        print(f"Skrapar: {url}")
        page = scrape_page(url)
        pages.append(page)
        print(f"  → {page['title']} ({len(page['content'])} tecken)")
    return pages

if __name__ == "__main__":
    pages = scrape_all()
    
    # Spara till fil
    with open("csn_data.json", "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)
    
    print(f"\nKlart! {len(pages)} sidor sparade till csn_data.json")