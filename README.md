# 🧾 RAG API Handover Notes

## ✅ What This Project Does
- Allows users to upload PDFs or .txt files
- Splits text into chunks and embeds them via `nomic-embed-text`
- Stores them in `pgvector` (PostgreSQL vector DB)
- On query, retrieves similar chunks and generates answers via `llama3:instruct` using Ollama

## 🧠 Key Components
- **FastAPI**: API routing and input validation
- **LangChain**: Splitting, embedding, similarity search
- **Ollama**: LLaMA 3.1 for LLM responses, nomic-embed-text for embeddings
- **PostgreSQL + pgvector**: Semantic DB backend

## 🚀 Deployment
```bash
ollama pull llama3:instruct
ollama pull nomic-embed-text
docker-compose up --build -d
