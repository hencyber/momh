# Studiestöd — Orhan Ulusoy

RAG-pipeline för CSN studiestöd (bidrag och lån).

## Vad gör den?
Chatbot som svarar på frågor om CSN:s studiestöd baserat på skrapad data från csn.se.

## Stack
- BeautifulSoup — scraping av csn.se/bidrag-och-lan/
- HuggingFace sentence-transformers — embeddings (multilingual)
- FAISS — vector store
- Claude Sonnet — LLM via Anthropic API
- FastAPI — REST API på port 8001

## Kom igång

1. Installera:
```bash
pip install -r requirements.txt
```

2. Skapa `.env`:

ANTHROPIC_API_KEY=din-nyckel

3. Bygg vector store:
```bash
python rag/pipeline.py
```

4. Starta server:
```bash
python -m uvicorn main:app --reload --port 8001
```

5. Öppna: http://localhost:8001

## MLflow
```bash
python rag/mlflow_tracking.py  # prompt versioning
python rag/evaluation.py       # automatisk evaluering
python -m mlflow ui            # öppna http://localhost:5000
```

## Filstruktur
backend/
├── main.py              # FastAPI app
├── rag/
│   ├── pipeline.py      # scraper + chunker + embeddings
│   ├── retriever.py     # sökning + Claude-anrop
│   ├── evaluation.py    # automatisk svarsutvärdering
│   └── mlflow_tracking.py
└── templates/
└── index.html       # webb-UI