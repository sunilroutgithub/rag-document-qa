
# from pypdf import PdfReader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import FakeEmbeddings
# from dotenv import load_dotenv
# import os

# load_dotenv()

# def get_embeddings():
#     return FakeEmbeddings(size=384)

# def load_pdf(file_path: str) -> str:
#     reader = PdfReader(file_path)
#     text = ""
#     for page in reader.pages:
#         text += page.extract_text() or ""
#     return text

# def split_text(text: str):
#     # SMALLER CHUNKS to reduce memory
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,      # Reduced from 1000
#         chunk_overlap=100    # Reduced from 200
#     )
#     return splitter.split_text(text)

# def create_vector_store(chunks: list, save_path: str = "faiss_index"):
#     embeddings = get_embeddings()
#     # Process chunks in smaller batches
#     batch_size = 50
#     for i in range(0, len(chunks), batch_size):
#         batch = chunks[i:i+batch_size]
#         if i == 0:
#             vector_store = FAISS.from_texts(batch, embedding=embeddings)
#         else:
#             temp_store = FAISS.from_texts(batch, embedding=embeddings)
#             vector_store.merge_from(temp_store)
#     vector_store.save_local(save_path)
#     return vector_store

# def load_vector_store(save_path: str = "faiss_index"):
#     embeddings = get_embeddings()
#     return FAISS.load_local(
#         save_path,
#         embeddings,
#         allow_dangerous_deserialization=True
#     )

# def ingest_pdf(file_path: str):
#     print(f"Loading PDF: {file_path}")
#     text = load_pdf(file_path)
#     print(f"Extracted {len(text)} characters")
#     chunks = split_text(text)
#     print(f"Created {len(chunks)} chunks")
#     store = create_vector_store(chunks)
#     print("Vector store created successfully!")
#     return store



from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings
from dotenv import load_dotenv
import os
import docx  # For DOCX support

load_dotenv()

def get_embeddings():
    return FakeEmbeddings(size=384)

def load_pdf(file_path: str) -> str:
    """Extract text from PDF file."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def load_docx(file_path: str) -> str:
    """Extract text from DOCX file."""
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def load_txt(file_path: str) -> str:
    """Extract text from TXT file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_document(file_path: str) -> str:
    """Load text from any supported document type."""
    if file_path.endswith('.pdf'):
        return load_pdf(file_path)
    elif file_path.endswith('.docx'):
        return load_docx(file_path)
    elif file_path.endswith('.txt'):
        return load_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

def split_text(text: str):
    """Split text into chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_text(text)

def create_vector_store(chunks: list, save_path: str = "faiss_index"):
    """Create FAISS vector store from text chunks."""
    embeddings = get_embeddings()
    # Process chunks in smaller batches
    batch_size = 50
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        if i == 0:
            vector_store = FAISS.from_texts(batch, embedding=embeddings)
        else:
            temp_store = FAISS.from_texts(batch, embedding=embeddings)
            vector_store.merge_from(temp_store)
    vector_store.save_local(save_path)
    return vector_store

def load_vector_store(save_path: str = "faiss_index"):
    """Load existing FAISS vector store."""
    embeddings = get_embeddings()
    return FAISS.load_local(
        save_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

def ingest_document(file_path: str):
    """Full pipeline: Document → chunks → vector store."""
    print(f"Loading document: {file_path}")
    text = load_document(file_path)
    print(f"Extracted {len(text)} characters")
    chunks = split_text(text)
    print(f"Created {len(chunks)} chunks")
    store = create_vector_store(chunks)
    print("Vector store created successfully!")
    return store