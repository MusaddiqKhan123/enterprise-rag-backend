from fastapi import APIRouter, UploadFile, File, HTTPException
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.db.pgvector_store import insert_document
import fitz  # PyMuPDF

router = APIRouter()

def extract_text(file: UploadFile) -> str:
    if file.filename.endswith(".pdf"):
        doc = fitz.open(stream=file.file.read(), filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
        return text
    elif file.filename.endswith(".txt"):
        return file.file.read().decode("utf-8")
    else:
        raise HTTPException(status_code=400, detail="Only .pdf and .txt files are supported")

@router.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    text = extract_text(file)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents([Document(page_content=text)])

    for i, doc in enumerate(docs):
        doc.metadata = {"chunk": i, "source": file.filename}

    insert_document(docs)

    return {"status": "success", "chunks_uploaded": len(docs)} 