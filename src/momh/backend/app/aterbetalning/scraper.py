import requests
from bs4 import BeautifulSoup
import json
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# CSN-sidor om återbetalning av studielån
CSN_URLS = [
    "https://www.csn.se/fragor-och-svar/hur-mycket-ska-jag-betala-pa-mitt-lan-i-ar.html",
    "https://www.csn.se/fragor-och-svar/hur-lange-ska-jag-betala-pa-mitt-lan.html",
    "https://www.csn.se/fragor-och-svar/hur-har-ni-raknat-ut-vad-jag-ska-betala-tillbaka-pa-mitt-studielan-i-ar.html",
    "https://www.csn.se/fragor-och-svar/hur-gor-jag-om-jag-vill-betala-en-gang-per-manad.html",
    "https://www.csn.se/fragor-och-svar/kan-jag-betala-tillbaka-hela-lanet-pa-en-gang.html",
    "https://www.csn.se/fragor-och-svar/kan-jag-skjuta-upp-min-aterbetalning-till-nasta-ar.html",
    "https://www.csn.se/fragor-och-svar/maste-jag-betala-pa-mitt-studielan-nar-jag-ar-arbetslos-eller-foraldraledig.html",
    "https://www.csn.se/fragor-och-svar/kan-jag-ansoka-om-att-betala-mindre-for-nasta-ar.html",
    "https://www.csn.se/fragor-och-svar/kan-jag-betala-innan-jag-ar-aterbetalningsskyldig.html",
    "https://www.csn.se/fragor-och-svar/har-du-fatt-ett-slutligt-arsbelopp-som-ska-betalas-under-2026.html",
]


def scrape_page(url):
    """skrapar en CSN-sida och returnerar titel + text"""
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    
    title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "Ingen titel"
    
    paragraphs = soup.find_all("p")
    content = " ".join([p.get_text(strip=True) for p in paragraphs])
    
    return {
        "url": url,
        "title": title,
        "content": content
    }


def scrape_all():
    """skrapar alla sidor i listan"""
    pages = []
    for url in CSN_URLS:
        print(f"Skrapar: {url}")
        try:
            page = scrape_page(url)
            pages.append(page)
            print(f"  -> {page['title']} ({len(page['content'])} tecken)")
        except Exception as e:
            print(f"  -> FEL: {e}")
    return pages


if __name__ == "__main__":
    pages = scrape_all()
    
    # spara till json
    os.makedirs("backend/data/aterbetalning", exist_ok=True)
    with open("backend/data/aterbetalning/csn_aterbetalning.json", "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)
    
    print(f"\n{len(pages)} sidor sparade")
