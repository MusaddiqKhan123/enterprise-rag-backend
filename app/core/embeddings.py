import os
from dotenv import load_dotenv
from langchain_ollama.embeddings import OllamaEmbeddings

load_dotenv()

ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
embedding_model = OllamaEmbeddings(model="nomic-embed-text", base_url=ollama_base_url)