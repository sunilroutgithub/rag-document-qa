

# from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import shutil
# import os
# from app.ingest import ingest_pdf, load_vector_store
# from app.rag import answer_question
# import threading

# app = FastAPI(
#     title="RAG Document Q&A API",
#     description="Upload PDFs and ask questions with source citations",
#     version="1.0.0"
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# UPLOAD_DIR = "data"
# FAISS_INDEX = "faiss_index"

# os.makedirs(UPLOAD_DIR, exist_ok=True)

# # Store processing status
# processing_status = {"status": "idle", "message": ""}

# class QuestionRequest(BaseModel):
#     question: str

# class AnswerResponse(BaseModel):
#     answer: str
#     sources: list
#     total_sources: int

# def process_pdf_background(file_path: str):
#     """Process PDF in background to avoid timeout."""
#     global processing_status
#     try:
#         processing_status = {"status": "processing", "message": "Processing PDF..."}
#         ingest_pdf(file_path)
#         processing_status = {"status": "ready", "message": "PDF processed successfully!"}
#     except Exception as e:
#         processing_status = {"status": "error", "message": str(e)}

# @app.get("/")
# def root():
#     return {
#         "message": "RAG Document Q&A API is running",
#         "docs": "/docs",
#         "status": processing_status
#     }

# @app.get("/health")
# def health_check():
#     index_exists = os.path.exists(FAISS_INDEX)
#     return {
#         "status": "healthy",
#         "vector_store_ready": index_exists,
#         "processing": processing_status
#     }

# @app.post("/upload")
# async def upload_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
#     """Upload a PDF and ingest it into the vector store."""
#     if not file.filename.endswith((".pdf", ".docx", ".txt")):
#     raise HTTPException(
#         status_code=400,
#         detail="Only PDF, DOCX, and TXT files are supported"
#     )
    
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
    
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
    
#     # Process in background
#     background_tasks.add_task(process_pdf_background, file_path)
    
#     return {
#         "message": f"Uploaded {file.filename}. Processing in background...",
#         "filename": file.filename,
#         "status": "processing"
#     }

# @app.post("/ask", response_model=AnswerResponse)
# async def ask_question(request: QuestionRequest):
#     """Ask a question about uploaded documents."""
#     if not os.path.exists(FAISS_INDEX):
#         raise HTTPException(
#             status_code=400,
#             detail="No documents uploaded yet. Please upload a PDF first."
#         )
    
#     if processing_status["status"] == "processing":
#         raise HTTPException(
#             status_code=202,
#             detail="PDF is still processing. Please wait a moment..."
#         )
    
#     try:
#         vector_store = load_vector_store(FAISS_INDEX)
#         result = answer_question(request.question, vector_store)
#         return AnswerResponse(
#             answer=result["answer"],
#             sources=result["sources"],
#             total_sources=result["total_sources"]
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))





from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from app.ingest import ingest_document, load_vector_store
from app.rag import answer_question

app = FastAPI(
    title="RAG Document Q&A API",
    description="Upload PDFs, DOCX, or TXT files and ask questions with source citations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data"
FAISS_INDEX = "faiss_index"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Store processing status
processing_status = {"status": "idle", "message": ""}

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    sources: list
    total_sources: int

def process_document_background(file_path: str):
    """Process document in background to avoid timeout."""
    global processing_status
    try:
        processing_status = {"status": "processing", "message": "Processing document..."}
        ingest_document(file_path)
        processing_status = {"status": "ready", "message": "Document processed successfully!"}
    except Exception as e:
        processing_status = {"status": "error", "message": str(e)}

@app.get("/")
def root():
    return {
        "message": "RAG Document Q&A API is running",
        "docs": "/docs",
        "status": processing_status
    }

@app.get("/health")
def health_check():
    index_exists = os.path.exists(FAISS_INDEX)
    return {
        "status": "healthy",
        "vector_store_ready": index_exists,
        "processing": processing_status
    }

@app.post("/upload")
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Upload a document (PDF, DOCX, TXT) and ingest it into the vector store."""
    if not file.filename.endswith((".pdf", ".docx", ".txt")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX, and TXT files are supported"
        )
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process in background
    background_tasks.add_task(process_document_background, file_path)
    
    return {
        "message": f"Uploaded {file.filename}. Processing in background...",
        "filename": file.filename,
        "status": "processing"
    }

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question about uploaded documents."""
    if not os.path.exists(FAISS_INDEX):
        raise HTTPException(
            status_code=400,
            detail="No documents uploaded yet. Please upload a document first."
        )
    
    if processing_status["status"] == "processing":
        raise HTTPException(
            status_code=202,
            detail="Document is still processing. Please wait a moment..."
        )
    
    try:
        vector_store = load_vector_store(FAISS_INDEX)
        result = answer_question(request.question, vector_store)
        return AnswerResponse(
            answer=result["answer"],
            sources=result["sources"],
            total_sources=result["total_sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))