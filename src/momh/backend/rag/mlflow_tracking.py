# Promptversionering och experiment-tracking med MLflow (Orhan – Studiestöd)
# Loggar olika prompt-versioner med svar och relevans-scores för jämförelse.
# Kör 'make mlflow' för att öppna MLflow UI och se resultaten.

from pathlib import Path

import mlflow
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

# Sätt MLflow-experiment för studiestöds-RAG
mlflow.set_experiment("csn-studiestod-rag")

# Version 1 av prompten
PROMPT_V1 = """Du är en hjälpsam assistent som svarar på frågor om CSN.
Basera ditt svar ENDAST på följande information från CSN:
{context}
Fråga: {question}
Svara på svenska och var tydlig och konkret."""

# Version 2 av prompten (förbättrad)
PROMPT_V2 = """Du är en kunnig och hjälpsam CSN-assistent som specialiserar sig på studiestöd, bidrag och lån.

Ditt uppdrag:
- Svara alltid på svenska
- Basera dina svar ENDAST på den information som ges i kontexten
- Om frågan är vag, ställ en följdfråga för att förstå situationen bättre
- Ge konkreta och specifika svar — undvik att säga "kontakta CSN" om svaret finns i kontexten
- Om informationen verkligen saknas i kontexten, var ärlig om det men förklara vad du vet
- Strukturera längre svar med punktlistor för tydlighet
- Håll en vänlig och professionell ton"""

def log_prompt_version(version: str, prompt: str, question: str, answer: str, relevance_score: float):
    # Logga en prompt-version med svar och relevans-score till MLflow
    with mlflow.start_run(run_name=f"prompt_{version}"):
        mlflow.log_param("prompt_version", version)
        mlflow.log_param("question", question)
        mlflow.log_text(prompt, f"prompt_{version}.txt")
        mlflow.log_text(answer, f"answer_{version}.txt")
        mlflow.log_metric("relevance_score", relevance_score)
        print(f"Loggat prompt {version} med relevans-score: {relevance_score}")


if __name__ == "__main__":
    from retriever import answer_question, load_vector_store

    question = "Hur mycket studiemedel kan jag få?"

    # Ladda vector store en gång och återanvänd för svaret
    print("Kör fråga mot RAG...")
    vector_store = load_vector_store()
    result = answer_question(question, vector_store)
    answer = result["answer"]

    # Logga v1 och v2 med manuellt satta scores
    log_prompt_version("v1", PROMPT_V1, question, answer, relevance_score=0.6)
    log_prompt_version("v2", PROMPT_V2, question, answer, relevance_score=0.85)
    
    print("\nKlart! Kör 'mlflow ui' för att se resultaten i webbläsaren.")