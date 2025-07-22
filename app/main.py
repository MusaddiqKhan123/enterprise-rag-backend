from fastapi import FastAPI
from app.api.v1 import upload, chat

app = FastAPI(title="RAG with FastAPI + pgvector + Ollama")

app.include_router(upload.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")