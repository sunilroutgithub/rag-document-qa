FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir \
    fastapi==0.138.1 \
    uvicorn==0.49.0 \
    python-multipart==0.0.32 \
    pypdf==6.14.2 \
    python-dotenv==1.2.2 \
    pydantic==2.13.4 \
    langchain-groq==1.1.3 \
    faiss-cpu==1.9.0.post1 \
    langchain==1.3.11 \
    langchain-community==0.4.2 \
    langchain-core==1.4.8 \
    langchain-text-splitters==1.1.2

COPY . .

RUN mkdir -p data faiss_index

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]