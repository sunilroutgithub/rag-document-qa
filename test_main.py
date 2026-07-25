import pytest

# Import the functions and classes to be tested
from app.main import process_document_background, root, serve_ui, health_check, upload_document, ask_question

# Define test fixtures
@pytest.fixture
def mock_file_path(tmp_path):
    return tmp_path / "test_file.pdf"

# Define test functions
def test_process_document_background(mock_file_path):
    # Test the process_document_background function
    process_document_background(mock_file_path)

def test_root():
    # Test the root function
    root()

def test_serve_ui():
    # Test the serve_ui function
    serve_ui()

def test_health_check():
    # Test the health_check function
    health_check()

def test_upload_document(mock_file_path):
    # Test the upload_document function
    upload_document(mock_file_path)

def test_ask_question():
    # Test the ask_question function
    ask_question(QuestionRequest(question="Test question"))

# Run the tests
def test_all():
    test_process_document_background()
    test_root()
    test_serve_ui()
    test_health_check()
    test_upload_document()
    test_ask_question()

if __name__ == "__main__":
    pytest.main(["-v", "test_main.py"])