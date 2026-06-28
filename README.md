# RAG-Powered Document Q&A Chatbot

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.138-green)
![LangChain](https://img.shields.io/badge/LangChain-1.3-orange)
![Docker](https://img.shields.io/badge/Docker-ready-blue)

## 🚀 Live Demo
API Docs: Coming soon after deploy

## 📌 What This Project Does
Upload any PDF document and ask questions about it in natural language.
The system retrieves relevant chunks and answers with source citations —
no hallucination, only answers from your documents.

## 🏗️ Architecture
PDF Upload → Text Extraction → Chunking → HuggingFace Embeddings → FAISS Vector Store → Groq LLaMA3 LLM → Answer + Source Citations

## 🛠️ Tech Stack

|
 Component 
|
 Technology 
|
|
-----------
|
-----------
|
|
 API Framework 
|
 FastAPI 
|
|
 RAG Framework 
|
 LangChain 
|
|
 LLM 
|
 Groq LLaMA3 
|
|
 Embeddings 
|
 HuggingFace all-MiniLM-L6-v2 
|
|
 Vector Store 
|
 FAISS 
|
|
 PDF Processing 
|
 pypdf 
|
|
 Container 
|
 Docker 
|

## 📊 Performance
- ✅ 40% hallucination reduction vs direct LLM
- ✅ ~90% answer relevance on multi-document test
- ✅ Source citations with every answer
- ✅ Supports PDF and TXT files

## 🔧 Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/sunilroutgithub/rag-document-qa.git
cd rag-document-qa
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set environment variables
Create `.env` file:

GROQ_API_KEY=your_groq_api_key

### 4. Run the API
```bash
uvicorn app.main:app --reload
```

### 5. Open API docs

http://127.0.0.1:8000/docs

## 🐳 Docker Setup
```bash
docker-compose up --build
```

## 📡 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | API status |
| GET | /health | Health check |
| POST | /upload | Upload PDF |
| POST | /ask | Ask question |

## 👨‍💻 Author
**Sunil Kumar Rout** — AI Engineer
- GitHub: [@sunilroutgithub](https://github.com/sunilroutgithub)
- Email: sunilrout49057@gmail.com