# Makefile för CSN Chatbot-projekt
# Kör 'make help' för att se alla tillgängliga kommandon.

.PHONY: help install setup-orhan setup-henke setup-mona \
        run-orhan run-henke run-mona run-all mlflow clean

help:
	@echo ""
	@echo "CSN Chatbot – tillgängliga kommandon:"
	@echo ""
	@echo "  make install        Installera alla Python-dependencies"
	@echo "  make setup-orhan    Bygg FAISS vector store för Studiestöd (Orhan)"
	@echo "  make setup-henke    Bygg FAISS vector store för Återbetalning (Henke)"
	@echo "  make setup-mona     Bygg ChromaDB vector store för Utlandsstudier (Mona)"
	@echo ""
	@echo "  make run-orhan      Starta Studiestöd API       (port 8001)"
	@echo "  make run-henke      Starta Återbetalning API    (port 8002)"
	@echo "  make run-mona       Starta Utlandsstudier API   (port 8003)"
	@echo "  make run-all        Starta alla tre backends"
	@echo ""
	@echo "  make mlflow         Starta MLflow UI            (port 5000)"
	@echo "  make clean          Rensa __pycache__ och .pyc-filer"
	@echo ""

# Installera dependencies från requirements.txt
install:
	pip install -r backend/requirements.txt

# Bygg FAISS vector store för Orhans studiestöds-backend
setup-orhan:
	@echo ">>> Bygger FAISS vector store för Studiestöd (Orhan)..."
	cd backend && python rag/pipeline.py
	@echo ">>> Klart! Vector store sparad i backend/csn_vector_store/"

# Bygg FAISS vector store för Henkes återbetalnings-backend
# TODO (Henke): Lägg till CSN-URLs i backend/aterbetalning/rag/pipeline.py
setup-henke:
	@echo ">>> Bygger FAISS vector store för Återbetalning (Henke)..."
	cd backend/aterbetalning && python rag/pipeline.py
	@echo ">>> Klart!"

# Bygg ChromaDB vector store för Monas utlandsstudier-backend
# TODO (Mona): Implementera pipeline.py och uppdatera det här target
setup-mona:
	@echo ">>> Bygger ChromaDB vector store för Utlandsstudier (Mona)..."
	@echo "    OBS: backend/data/ är gitignorerad – data byggs lokalt."
	cd backend/utlandsstudier && python rag/pipeline.py
	@echo ">>> Klart! ChromaDB sparad i backend/data/chroma_utlandsstudier/"

# Starta Orhans backend (Studiestöd, port 8001)
run-orhan:
	@echo ">>> Startar Studiestöd API på http://localhost:8001 ..."
	cd backend && uvicorn main:app --reload --port 8001

# Starta Henkes backend (Återbetalning, port 8002)
run-henke:
	@echo ">>> Startar Återbetalning API på http://localhost:8002 ..."
	cd backend/aterbetalning && uvicorn main:app --reload --port 8002

# Starta Monas backend (Utlandsstudier, port 8003)
run-mona:
	@echo ">>> Startar Utlandsstudier API på http://localhost:8003 ..."
	cd backend/utlandsstudier && uvicorn main:app --reload --port 8003

# Starta alla tre backends (kräver att alla vector stores är byggda)
run-all:
	@echo ">>> Startar alla tre backends..."
	@echo "    Använd Ctrl+C för att stoppa."
	cd backend && uvicorn main:app --port 8001 & \
	cd backend/aterbetalning && uvicorn main:app --port 8002 & \
	cd backend/utlandsstudier && uvicorn main:app --port 8003

# Starta MLflow UI för att se experimentresultat
mlflow:
	@echo ">>> Startar MLflow UI på http://localhost:5000 ..."
	cd backend && mlflow ui --port 5000

# Rensa cache-filer
clean:
	@echo ">>> Rensar __pycache__ och .pyc-filer..."
	find . -type d -name "__pycache__" -not -path "./.git/*" -exec rm -rf {} + 2>/dev/null; true
	find . -name "*.pyc" -not -path "./.git/*" -delete 2>/dev/null; true
	@echo ">>> Klart!"
