import os
import sys
from pathlib import Path
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import shutil
import time
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from backend.app.tools.vector_db import get_vector_store
from backend.app.db.database import get_db
from backend.app.db.models import User, DocumentMetadata
from backend.app.tools.generate_docs_metadata import generate_document_metadata
router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def ingest_document(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    1. Saves the uploaded PDF.
    2. Reads and chunks the text.
    3. Generates metadata for the document.
    4. Embeds and stores it in ChromaDB (Vector Store).
    """
    # SECURITY CHECK: Only Admins or HRs can upload knowledge documents.
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.role.name not in ["admin", "hr"]:
        raise HTTPException(
            status_code=403, 
            detail="Forbidden: Only Admins or HRs can upload knowledge documents."
        )

    try:
        # 1. Save File Temporarily
        file_path = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. Load & Split PDF
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        # Combine the pages to give the AI enough context
        full_text = "\n".join([doc.page_content for doc in docs])

        # We await the async function you built
        ai_insights = await generate_document_metadata(full_text)

        # This builds your 'Library Catalog' for the Orchestrator
        db_doc = DocumentMetadata(
            filename=file.filename,
            summary=ai_insights["summary"],
            keywords=ai_insights["keywords"]
        )
        db.add(db_doc)
        db.commit()

        # Split into smaller chunks (better for RAG)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        # 3. Add Metadata (Crucial for filtering later!)
        for split in splits:
            split.metadata["source"] = file.filename
            split.metadata["uploaded_at"] = time.strftime("%Y-%m-%d %H:%M:%S")

        # 4. Push to ChromaDB
        vector_store = get_vector_store()
        vector_store.add_documents(splits)

        # Cleanup: remove local file after indexing
        os.remove(file_path)

        return {
           "message": f"Successfully indexed {len(splits)} chunks.",
            "filename": file.filename,
            "ai_insights": ai_insights # Return this so the frontend can display it!
        }

    except Exception as e:
        db.rollback() # Rollback the transaction if something goes wrong
        raise HTTPException(status_code=500, detail=str(e))