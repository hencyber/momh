import mlflow
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")

# Sätt experiment-namn
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
    with mlflow.start_run(run_name=f"prompt_{version}"):
        # Logga prompt-parametrar
        mlflow.log_param("prompt_version", version)
        mlflow.log_param("question", question)
        
        # Logga prompten som artifact
        mlflow.log_text(prompt, f"prompt_{version}.txt")
        
        # Logga svaret
        mlflow.log_text(answer, f"answer_{version}.txt")
        
        # Logga betyg
        mlflow.log_metric("relevance_score", relevance_score)
        
        print(f"Loggat prompt {version} med relevans-score: {relevance_score}")

if __name__ == "__main__":
    from retriever import answer_question
    
    question = "Hur mycket studiemedel kan jag få?"
    
    # Testa och logga båda versionerna
    print("Kör fråga mot RAG...")
    result = answer_question(question)
    answer = result["answer"]
    
    # Logga v1 och v2 med manuellt satta scores
    log_prompt_version("v1", PROMPT_V1, question, answer, relevance_score=0.6)
    log_prompt_version("v2", PROMPT_V2, question, answer, relevance_score=0.85)
    
    print("\nKlart! Kör 'mlflow ui' för att se resultaten i webbläsaren.")