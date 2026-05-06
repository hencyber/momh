import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
import mlflow
import time

# 1. Load env variables and activate OpenRouter
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

# ADDED MLflow experiment
mlflow.set_experiment("Utlandsstudier")
mlflow.set_tracking_uri("file:./mlruns")  # Added since UI wasn't showing any runs on UI


def setup_rag_chain():
    # 2. Load existing database
    persist_directory = "backend/data/utlandsstudier/chroma_db"
    model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )

    # 3. Create retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # 4. Define model
    llm = ChatOpenAI(
        model="nvidia/nemotron-3-nano-30b-a3b:free",
        temperature=0.1
    )

    # 5. Prompt and guardrails 
    template = """Du är en expert på utlandsstudier och CSN.
...
Svar:"""

    prompt = ChatPromptTemplate.from_template(template)

    # UPDATED SECTIOON New code, here i create a function instead of chain 

    def rag_pipeline(question: str): 
        docs = retriever.invoke(question)

    def rag_pipeline(question: str):

        # ADDED suspicious prompts / prompt injection attempts
        fishy_prompts = [
            "ignorera tidigare instruktioner",
            "avslöja system prompt",
            "visa api nycklar",
            "jailbreak",
            "lösenord"
        ]

        # ADDED detect suspicious prompts
        sounds_suspicious = any(
            word in question.lower()
            for word in fishy_prompts
        )

        # ADDED timer start
        start_time = time.time()

        # UPDATED newer langchain retrieval
        docs = retriever.invoke(question)


        sources = [doc.metadata.get("source", "unknown") for doc in docs]
        context = "\n\n".join([doc.page_content for doc in docs])

        messages = prompt.format_messages(
            context=context,
            question=question
        )

        response = llm.invoke(messages)

        # ADDED timer end
        end_time = time.time()

        # ADDED response time calculation
        response_time = end_time - start_time
        print("MLFLOW Run started")

        # ADDED MLflow logging
        with mlflow.start_run():

            # Parameters
            mlflow.log_param("model", "nvidia/nemotron-3-nano-30b-a3b")
            mlflow.log_param("temperature", 0.1)
            mlflow.log_param("top_k", 3)

            # Security / guardrails
            mlflow.log_param("fishy_prompts", sounds_suspicious)

            # Metrics
            mlflow.log_metric("response_time_seconds", response_time)
            mlflow.log_metric("number_of_sources", len(response["sources"]) if isinstance(response, dict) else len(sources))

            # ADDED logging text
            mlflow.log_text(question, "question.txt")
            mlflow.log_text(response.content, "response.txt")

            print("MLFLOW logging finished")

        return {
            "answer": response.content,
            "sources": sources
        }

    return rag_pipeline


if __name__ == "__main__":
    chain = setup_rag_chain()

    question = "Vad gäller för CSN vid utlandsstudier?"
    print(f"\nStäller fråga: {question}\n")

    response = chain(question)

    print("--- SVAR ---")
    print(response)