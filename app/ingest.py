from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

def load_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def split_text(text: str):
    """Split text into chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_text(text)

def create_vector_store(chunks: list, save_path: str = "faiss_index"):
    """Create FAISS vector store from text chunks."""
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local(save_path)
    return vector_store

def load_vector_store(save_path: str = "faiss_index"):
    """Load existing FAISS vector store."""
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    return FAISS.load_local(
        save_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

def ingest_pdf(file_path: str):
    """Full pipeline: PDF → chunks → vector store."""
    print(f"Loading PDF: {file_path}")
    text = load_pdf(file_path)
    print(f"Extracted {len(text)} characters")
    chunks = split_text(text)
    print(f"Created {len(chunks)} chunks")
    store = create_vector_store(chunks)
    print("Vector store created successfully!")
    return store