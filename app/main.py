import pytest

# Test process_document_background function
def test_process_document_background(tmp_path):
    # Create a temporary file
    file_path = tmp_path / "document.pdf"
    file_path.write_bytes(b"Document content")

    # Call process_document_background function
    process_document_background(str(file_path))

    # Check processing status
    assert processing_status == {"status": "ready", "message": "Document processed successfully!"}

# Test root function
def test_root(tmp_path):
    # Create a temporary index.html file
    index_html_path = tmp_path / "index.html"
    index_html_path.write_text("<h1>\u2708 RAG Document Q&A API is running</h1><p>Landing page not found.</p>")

    # Call root function
    response = root()

    # Check response status code
    assert response.status_code == 404

    # Check response content
    assert response.content == b"<h1>\u2708 RAG Document Q&A API is running</h1><p>Landing page not found.</p>"

# Test serve_ui function
def test_serve_ui(tmp_path):
    # Create a temporary frontend.html file
    frontend_html_path = tmp_path / "frontend.html"
    frontend_html_path.write_text("<h1>UI file not found</h1>")

    # Call serve_ui function
    response = serve_ui()

    # Check response status code
    assert response.status_code == 404

    # Check response content
    assert response.content == b"<h1>UI file not found</h1>"

# Test health_check function
def test_health_check(tmp_path):
    # Create a temporary FAISS index file
    faiss_index_path = tmp_path / "faiss_index"
    faiss_index_path.write_bytes(b"FAISS index content")

    # Call health_check function
    response = health_check()

    # Check response status code
    assert response == {"status": "healthy", "vector_store_ready": True, "processing": {"status": "idle", "message": ""}}

# Test upload_document function
def test_upload_document(tmp_path):
    # Create a temporary file
    file_path = tmp_path / "document.pdf"
    file_path.write_bytes(b"Document content")

    # Call upload_document function
    response = upload_document(background_tasks=BackgroundTasks(), file=UploadFile(file_path))

    # Check response status code
    assert response == {"message": "Uploaded document.pdf. Processing in background...", "filename": "document.pdf", "status": "processing"}

# Test ask_question function
def test_ask_question(tmp_path):
    # Create a temporary FAISS index file
    faiss_index_path = tmp_path / "faiss_index"
    faiss_index_path.write_bytes(b"FAISS index content")

    # Call ask_question function
    response = ask_question(request=QuestionRequest(question="What is the answer?"))

    # Check response status code
    assert response == AnswerResponse(answer="The answer is unknown.", sources=[], total_sources=0)
