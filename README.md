# CSN Chatbot — LLMOps Grupprojekt

RAG-baserad chatbot som svarar på frågor om CSN (Centrala studiestödsnämnden).
Byggd av Orhan, Henke, Mona och Marian som del av YH-kursen LLMOps/AI Engineering.

---

## Arkitektur

Varje domän är en självständig FastAPI-applikation med sin egna RAG-pipeline:

Fråga från användaren
│
▼
[1] Embedding + Similarity Search  ←── Vector Store (FAISS/ChromaDB)
│
▼
[2] Kontext hämtas (top-k chunks)
│
▼
[3] Claude genererar svar baserat på kontexten
│
▼
{ "answer": "...", "sources": [...] }

| Backend            | Ansvarig | Teknologi | Port |
|--------------------|----------|-----------|------|
| Studiestöd         | Orhan    | FAISS     | 8001 |
| Återbetalning      | Henke    | FAISS     | 8002 |
| Utlandsstudier     | Mona     | ChromaDB  | 8003 |
| DevOps/Integration | Marian   | Docker    | —    |

---

## Kom igång (lokalt)

### Förutsättningar
- Python 3.11+
- En Anthropic API-nyckel ([skaffa här](https://console.anthropic.com/))
- make installerat (Windows: via Git Bash eller WSL)

### 1. Klona repot
```bash
git clone https://github.com/hencyber/momh.git
cd momh
```

### 2. Sätt upp miljövariabler
```bash
cp backend/.env.example backend/.env
# Öppna backend/.env och fyll i din API-nyckel
```

### 3. Installera dependencies
```bash
make install
```

### 4. Bygg vector stores
```bash
make setup-orhan
make setup-henke
make setup-mona
```

### 5. Starta backends
```bash
# En backend
make run-orhan

# Alla
make run-all
```

### 6. Öppna gränssnittet
Gå till http://localhost:8001 i webbläsaren.

---

## Miljövariabler

| Variabel          | Beskrivning           | Obligatorisk |
|-------------------|-----------------------|:------------:|
| ANTHROPIC_API_KEY | API-nyckel för Claude | ✅           |

Committa aldrig .env — den är gitignorerad.

---

## Kör med Docker

Docker-konfiguration hanteras av Marian.

---

## API-kontrakt

Se API_CONTRACT.md för detaljer.

**Request:**
POST /chat
{ "question": "Hur mycket kan jag låna?" }

**Svar:**
{ "answer": "...", "sources": ["https://www.csn.se/..."] }

---

## MLflow

```bash
make mlflow
# Öppna http://localhost:5000
```

---

## Projektstruktur

momh/
├── Makefile
├── API_CONTRACT.md
├── WAY_OF_WORKING.md
├── README.md
└── backend/
├── main.py
├── requirements.txt
├── .env.example
├── rag/
│   ├── pipeline.py
│   ├── retriever.py
│   ├── evaluation.py
│   └── mlflow_tracking.py
├── templates/
│   └── index.html
├── aterbetalning/
└── utlandsstudier/

---

## Gruppmedlemmar

| Namn   | Ansvarsområde             |
|--------|---------------------------|
| Orhan  | Studiestöd (port 8001)    |
| Henke  | Återbetalning (port 8002) |
| Mona   | Utlandsstudier (port 8003)|
| Marian | DevOps, slutintegration   |