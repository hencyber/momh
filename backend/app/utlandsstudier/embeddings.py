## LLM USAGE, Used LLM as assistance since i encountered numerous problems in this part

import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from chunker import load_chunk_text # Added 

def create_embeddings():
    print("Step 1: Starting create_embeddings...")
    input_file = "backend/data/utlandsstudier/csn_utlandsstudier.txt"
    persist_directory = "backend/data/utlandsstudier/chroma_db"

    
    if not os.path.exists(input_file):
        print(f"ERROR: Could not find the file {input_file}")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        text_data = f.read()
    
    chunks = load_chunk_text(input_file)  ## Added LMM USAGE 
    documents = [Document(page_content=chunk) for chunk in chunks]
    print(f"Step 2: Found {len(documents)} chunks. Creating embeddings (this may take a while)...")

    
    model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    embeddings_model = HuggingFaceEmbeddings(model_name=model_name)

    
    vector_db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings_model,
        persist_directory=persist_directory
    )
    print(f"Step 3: Wohoo! Database saved in {persist_directory}")


if __name__ == "__main__":
    create_embeddings()