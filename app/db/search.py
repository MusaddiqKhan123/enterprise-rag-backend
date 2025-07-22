import os
from langchain_community.vectorstores.pgvector import PGVector
from app.core.embeddings import embedding_model

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ragdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

def search_similar_documents(query_embedding, top_k=3):
    vectorstore = PGVector(
        collection_name="rag_chunks",
        connection_string=f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        embedding_function=embedding_model,
    )
    results = vectorstore.similarity_search_by_vector(query_embedding, k=top_k)
    return [(doc.page_content, doc.metadata) for doc in results]