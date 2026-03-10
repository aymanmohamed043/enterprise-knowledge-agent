import os
import sys
from pathlib import Path
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from fastapi import APIRouter
from backend.app.tools.vector_db import get_vector_store

router = APIRouter(prefix="/test_rag", tags=["Testing"])

@router.get("/test-retriever")
async def test_retriever_only(query: str, k: int = 3):
    """
    Pure retrieval test. No LLM involved.
    Returns the exact chunks ChromaDB finds for the query to verify indexing quality.
    """
    try:
        # 1. Connect to ChromaDB
        vector_store = get_vector_store()
        
        # 2. Perform the mathematical similarity search
        results = vector_store.similarity_search(query, k=k)
        
        # 3. Format the raw chunks for easy debugging
        formatted_results = []
        for i, doc in enumerate(results):
            formatted_results.append({
                "rank": i + 1,
                "metadata": doc.metadata, # This will show source, keywords, etc.
                "content_preview": doc.page_content[:300] + "...", # First 300 chars
                "full_content": doc.page_content
            })
            
        return {
            "query": query,
            "total_retrieved": len(results),
            "chunks": formatted_results
        }
    except Exception as e:
        return {"error": str(e)}