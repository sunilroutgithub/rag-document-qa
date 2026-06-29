from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

def get_embeddings():
    return FakeEmbeddings(size=384)

def load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def split_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_text(text)

def create_vector_store(chunks: list, save_path: str = "faiss_index"):
    embeddings = get_embeddings()
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local(save_path)
    return vector_store

def load_vector_store(save_path: str = "faiss_index"):
    embeddings = get_embeddings()
    return FAISS.load_local(
        save_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

def ingest_pdf(file_path: str):
    print(f"Loading PDF: {file_path}")
    text = load_pdf(file_path)
    print(f"Extracted {len(text)} characters")
    chunks = split_text(text)
    print(f"Created {len(chunks)} chunks")
    store = create_vector_store(chunks)
    print("Vector store created successfully!")
    return store