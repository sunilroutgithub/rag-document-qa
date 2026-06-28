from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm():
    """Initialize Groq LLM."""
    return ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3
    )

def format_docs(docs):
    """Format retrieved documents into single string."""
    return "\n\n".join(doc.page_content for doc in docs)

def load_vector_store_for_rag(save_path: str = "faiss_index"):
    """Load FAISS vector store with HuggingFace embeddings."""
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    return FAISS.load_local(
        save_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

def answer_question(question: str, vector_store: FAISS):
    """Answer question using RAG pipeline."""
    llm = get_llm()
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    prompt = PromptTemplate.from_template("""
You are a helpful assistant that answers questions based ONLY on the
provided document context. If the answer is not in the context,
say "I could not find this information in the provided documents."

Context:
{context}

Question:
{question}

Answer with clear explanation and mention which part of the
document supports your answer:
""")

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = chain.invoke(question)

    source_docs = retriever.invoke(question)
    sources = []
    for i, doc in enumerate(source_docs):
        sources.append({
            "chunk_number": i + 1,
            "content_preview": doc.page_content[:200] + "..."
        })

    return {
        "answer": answer,
        "sources": sources,
        "total_sources": len(sources)
    }