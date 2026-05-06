import requests
from bs4 import BeautifulSoup

URL= "https://www.csn.se/bidrag-och-lan/utlandsstudier-med-studiemedel.html"

def fetch_page(url):
    response= requests.get(url)

    response.raise_for_status()
    return response.text 

def parse_text(html):
    soup= BeautifulSoup(html, "html.parser")

    paragraphs= soup.find_all("p")
    text = "\n".join(p.get_text() for p in paragraphs)
    return text 


def save_text(text, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__": 
    html = fetch_page(URL)
    text= parse_text(html)
    save_text(text, "backend/data/utlandsstudier/csn_utlandsstudier.txt")
    print("Data sparad !")



