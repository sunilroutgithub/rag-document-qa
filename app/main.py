from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from app.ingest import ingest_pdf, load_vector_store
from app.rag import answer_question

app = FastAPI(
    title="RAG Document Q&A API",
    description="Upload PDFs and ask questions with source citations",
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

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    sources: list
    total_sources: int

@app.get("/")
def root():
    return {
        "message": "RAG Document Q&A API is running",
        "docs": "/docs",
        "endpoints": {
            "upload_pdf": "POST /upload",
            "ask_question": "POST /ask",
            "health": "GET /health"
        }
    }

@app.get("/health")
def health_check():
    index_exists = os.path.exists(FAISS_INDEX)
    return {
        "status": "healthy",
        "vector_store_ready": index_exists
    }

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF and ingest it into the vector store."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        ingest_pdf(file_path)
        return {
            "message": f"Successfully ingested {file.filename}",
            "filename": file.filename,
            "status": "ready"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question about uploaded documents."""
    if not os.path.exists(FAISS_INDEX):
        raise HTTPException(
            status_code=400,
            detail="No documents uploaded yet. Please upload a PDF first."
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