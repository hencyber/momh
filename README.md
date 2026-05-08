# CSN Chatbot (MLOps project - momh)

## Overview
This project is a chatbot system for CSN-related questions.
Each team member is responsible for a specific domain:

- Studiestöd
- Återbetalning
- Utlandsstudier

The system is built using Retrieval-Augmented Generation (RAG).


## Architecture
The project consists of:

- Backend (FastAPI + RAG logic)
- Frontend (user interface)
- Docker & Docker Compose for containerization
- GitHub Actions for CI


## How to run

```bash
docker compose up --build
```


## Project Structure

```text
momh/
├── backend/        # API + RAG logic
├── frontend/       # Chat UI
├── docker-compose.yml
└── .github/        # CI workflows
```


## Components

### Backend
Handles:
- RAG pipeline
- API endpoints
- communication with LLM

### Frontend
Handles:
- User interaction
- Sending questions to backend
- Displaying answers

### DevOps
Includes:
- Dockerfiles for services
- docker-compose setup
- CI with GitHub Actions


## Chatbot Domains

Each team member is responsible for a specific CSN domain:

### Studiestöd
To be added.

### Återbetalning

See detailed implementation below:
*Implemented by Henke*

# Återbetalning - CSN-Bot

Denna modul hanterar frågor om återbetalning av studielån från CSN.

## Vad den gör

1. Skrapar 10 sidor från csn.se om återbetalning (årsbelopp, ränta, uppskjutning, slutbetalning mm)
2. Delar upp texten i chunks och skapar en vektordatabas med FAISS
3. När en användare ställer en fråga söker den i vektordatabasen efter relevant information
4. Skickar frågan och kontexten till en LLM som genererar ett svar på svenska
5. Returnerar svaret tillsammans med källhänvisningar till vilka CSN-sidor svaret baseras på

## Filer

| Fil | Beskrivning |
|-----|-------------|
| `backend/app/aterbetalning/scraper.py` | Hämtar data från csn.se |
| `backend/app/aterbetalning/embeddings.py` | Chunkar text och skapar FAISS-vektordatabas |
| `backend/app/aterbetalning/rag.py` | RAG-pipeline med OpenRouter |
| `backend/app/aterbetalning/api.py` | FastAPI-endpoint POST /chat på port 8002 |
| `frontend/henke_test.py` | Streamlit-testsida för chatten |
| `backend/data/aterbetalning/` | Scrapad data och vektordatabas |

## Teknik

- **Embeddings:** HuggingFace (sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)
- **Vektordatabas:** FAISS
- **LLM:** OpenRouter (nvidia/nemotron-3-nano-30b-a3b:free)
- **API:** FastAPI
- **Frontend:** Streamlit

## Köra lokalt

### 1. Installera beroenden

```bash
pip install langchain langchain-community langchain-huggingface langchain-text-splitters faiss-cpu openai python-dotenv fastapi uvicorn streamlit
```

### 2. Skapa .env-fil i projektets rot

```
OPENROUTER_API_KEY=din-nyckel-här
```

API-nyckel skapas gratis på https://openrouter.ai

### 3. Starta backend

```bash
cd backend/app/aterbetalning
python api.py
```

API:t körs på http://localhost:8002

### 4. Testa med Streamlit (valfritt)

```bash
streamlit run frontend/henke_test.py
```

## API

**POST /chat**

Request:
```json
{
  "question": "Hur mycket ska jag betala tillbaka?"
}
```

Response:
```json
{
  "answer": "Ditt årsbelopp beräknas utifrån din inkomst...",
  "sources": ["https://csn.se/fragor-och-svar/..."]
}
```

**GET /health**

Returnerar `{"status": "ok"}`

### Utlandsstudier
To be added. 

Each domain has its own RAG pipeline and backend logic but follows a shared API structure for integration.


## DevOps & Infrastructure

This project uses containerization and CI to ensure a reproducible environment.

### Docker
- Each service runs in its own container
- backend and frontend are containerized using Dockerfiles

### Docker compose
- Used to run multiple services together
- Simplifies local development and testing

### CI (GitHub Actions)
- Automatically builds the backend Docker image
- Ensures that the project can run in a clean environment

This setup allows the team to develop independently while maintaining a unified system.


## How to run the project

Make sure Docker is installed and running.

Run the following command:

```bash
docker compose up --build
```

Then open in a browser:

http://localhost:8000


## Screenshots
** Placeholder **
Add screenshots here showing the running application


## NOTES

This project demonstrates how independent RAG-based services can be combined into a unified system using DevOps practices.
Each team member works on their own domain while maintaining a shared structure for integration.