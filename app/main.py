from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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

def process_document_background(file_path: str) -> None:
    """Process document in background to avoid timeout.

    Args:
        file_path (str): Path to the document file.

    Returns:
        None
    """
    global processing_status
    try:
        processing_status = {"status": "processing", "message": "Processing document..."}
        ingest_document(file_path)
        processing_status = {"status": "ready", "message": "Document processed successfully!"}
    except Exception as e:
        processing_status = {"status": "error", "message": str(e)}

@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    """Serve the professional landing page.

    Returns:
        HTMLResponse: The landing page HTML.
    """
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>\u2708 RAG Document Q&A API is running</h1><p>Landing page not found.</p>", status_code=404)

@app.get("/ui", response_class=HTMLResponse)
async def serve_ui() -> HTMLResponse:
    """Serve the interactive UI for uploading and asking questions.

    Returns:
        HTMLResponse: The UI HTML.
    """
    try:
        with open("app/frontend.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>UI file not found</h1>", status_code=404)

# ========== API ENDPOINTS ==========\n
@app.get("/health")
def health_check() -> dict:
    """Check the health of the API.

    Returns:
        dict: The health status.
    """
    index_exists = os.path.exists(FAISS_INDEX)
    return {"status": "healthy", "vector_store_ready": index_exists, "processing": processing_status}

@app.post("/upload")
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)) -> dict:
    """Upload a document (PDF, DOCX, TXT) and ingest it into the vector store.

    Args:
        background_tasks (BackgroundTasks): The background tasks.
        file (UploadFile): The uploaded file.

    Returns:
        dict: The upload status.
    """
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

    return {"message": f"Uploaded {file.filename}. Processing in background...", "filename": file.filename, "status": "processing"}

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest) -> AnswerResponse:
    """Ask a question about uploaded documents.

    Args:
        request (QuestionRequest): The question request.

    Returns:
        AnswerResponse: The answer response.
    """
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