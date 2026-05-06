import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

#Removed ! unused imports , StrOutputParser, RunnablePassthrough

# 1. Load env variables and activate OpenRouter
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"


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
        sources = [doc.metadata.get("source", "unknown") for doc in docs]
        context = "\n\n".join([doc.page_content for doc in docs])

        messages = prompt.format_messages(
            context=context,
            question=question
        )

        response = llm.invoke(messages)

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