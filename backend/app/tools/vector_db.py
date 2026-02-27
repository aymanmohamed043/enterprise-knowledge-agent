from langchain_chroma import Chroma
from pathlib import Path
import os
import sys

# Allow running this file directly (python backend/app/tools/vector_db.py)
# by ensuring the repo root is on sys.path for absolute imports.
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from backend.app.core.llm import SentenceTransformerEmbeddings

embeddings_model = SentenceTransformerEmbeddings()
# Define where Chroma stores data (matches docker-compose volume if running locally)
# Since we are running FastAPI locally (not in docker yet), we use a local folder
# OR connect to the HttpClient if you want to use the Docker container strictly.
# For simplicity in dev, let's use the Docker HTTP Client.

import chromadb
from chromadb.config import Settings

def get_vector_store():
    # Connect to the Chroma Container running on port 8001
    client = chromadb.HttpClient(host='localhost', port=8001)
    
    vector_store = Chroma(
        client=client,
        collection_name="enterprise_knowledge",
        embedding_function=embeddings_model
    )
    return vector_store

def search_documents(query: str):
    """
    Searches the vector database for relevant policies or documents.
    """
    vector_store = get_vector_store()
    # Search for top 3 most relevant chunks
    results = vector_store.similarity_search(query, k=3)
    
    # Format results as a string
    return "\n\n".join([doc.page_content for doc in results])



if __name__ == "__main__":
    # test search_documents
    print(search_documents("What is the skills ayman has?"))