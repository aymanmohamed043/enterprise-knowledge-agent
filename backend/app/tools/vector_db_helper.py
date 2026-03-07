import os
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
from dotenv import load_dotenv
load_dotenv(_REPO_ROOT / "backend" / ".env")

from sqlalchemy.orm import Session
from backend.app.db.models import DocumentMetadata

def get_knowledge_catalog(db: Session):
    """
    Fetches the AI-generated summaries of all ingested documents.
    This is used to help the Orchestrator decide if it should use the Vector Tool.
    """
    docs = db.query(DocumentMetadata).all()
    if not docs:
        return "No documents have been uploaded to the knowledge base yet."
    
    catalog = "AVAILABLE KNOWLEDGE DOCUMENTS:\n"
    for doc in docs:
        catalog += f"- File Name: {doc.filename}\n Summary: {doc.summary}\n  Keywords: {doc.keywords}\n\n"
        
    return catalog