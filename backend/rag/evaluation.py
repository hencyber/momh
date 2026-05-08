import mlflow
import anthropic
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")

client = anthropic.Anthropic()

mlflow.set_experiment("csn-studiestod-rag")

def evaluate_answer(question: str, answer: str, context: str) -> dict:
    """Låt Claude bedöma kvaliteten på ett svar automatiskt."""
    
    evaluation_prompt = f"""Du är en kvalitetsbedömare för en CSN-chatbot. 
Bedöm följande svar på en skala 0.0-1.0 inom tre kategorier.

Fråga: {question}

Kontext (information från CSN):
{context}

Svar från chatboten:
{answer}

Svara ENDAST med JSON i detta format, ingenting annat:
{{
    "relevance": 0.0,
    "correctness": 0.0,
    "conciseness": 0.0,
    "reasoning": "kort förklaring"
}}

Definitioner:
- relevance: Svarar chatboten på frågan som ställdes?
- correctness: Stämmer svaret med kontexten från CSN?
- conciseness: Är svaret lagom långt och tydligt?"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": evaluation_prompt}]
    )
    
    import json
    scores = json.loads(response.content[0].text)
    return scores

def run_evaluation(question: str, answer: str, context: str, prompt_version: str):
    """Kör evaluering och logga resultaten i MLflow."""
    
    print(f"Evaluerar svar för prompt {prompt_version}...")
    scores = evaluate_answer(question, answer, context)
    
    with mlflow.start_run(run_name=f"eval_{prompt_version}"):
        mlflow.log_param("prompt_version", prompt_version)
        mlflow.log_param("question", question)
        
        mlflow.log_metric("relevance", scores["relevance"])
        mlflow.log_metric("correctness", scores["correctness"])
        mlflow.log_metric("conciseness", scores["conciseness"])
        
        mlflow.log_text(answer, "answer.txt")
        mlflow.log_text(scores["reasoning"], "reasoning.txt")
        
        print(f"  Relevans:   {scores['relevance']}")
        print(f"  Korrekthet: {scores['correctness']}")
        print(f"  Koncishet:  {scores['conciseness']}")
        print(f"  Motivering: {scores['reasoning']}")
    
    return scores

if __name__ == "__main__":
    from retriever import answer_question, retrieve_context, load_vector_store
    
    question = "Hur mycket studiemedel kan jag få?"
    
    print("Hämtar svar från RAG...")
    vector_store = load_vector_store()
    context_docs = retrieve_context(question, vector_store)
    context = "\n\n".join([doc.page_content for doc in context_docs])
    
    result = answer_question(question)
    answer = result["answer"]
    
    run_evaluation(question, answer, context, prompt_version="v2")
    
    print("\nKlart! Öppna MLflow UI för att se evalueringen.")