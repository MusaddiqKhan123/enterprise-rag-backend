from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.embeddings import embedding_model  # ✅ Needed
from app.db.search import search_similar_documents  # ✅ NEW
from langchain_community.llms import Ollama
import os

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str

ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
llm = Ollama(model="llama3.1", base_url=ollama_base_url)

@router.post("/chat")
async def chat(req: ChatRequest):
    query_embedding = embedding_model.embed_query(req.prompt)
    results = search_similar_documents(query_embedding, top_k=3)

    if not results:
        raise HTTPException(status_code=404, detail="No relevant documents found")

    context = "\n".join([r[0] for r in results])
    rag_prompt = f"""
    You are an intelligent assistant. Use only the context provided below to answer the user's question accurately and concisely.
    ---
    {context}
    ---
    Question: {req.prompt}
    Answer:
    """

    answer = llm.invoke(rag_prompt)
    return {"response": answer}