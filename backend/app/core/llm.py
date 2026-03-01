from pathlib import Path
import sys

# Ensure the repo root is on sys.path so absolute imports work
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import os   
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from sentence_transformers import SentenceTransformer, util

load_dotenv()

# 1. The Chat Model (The Brain)
# We use 'flash' because it's fast for agents
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,  # 0 means "be factual", don't be creative
    convert_system_message_to_human=True
)

# 2. The Embeddings (The Translator for PDFs)
# This turns text into numbers for ChromaDB
class SentenceTransformerEmbeddings:
    def __init__(self, model_name="all-MiniLM-L6-v2", device="cpu"):
        self.model = SentenceTransformer(model_name, device=device)

    def embed_documents(self, texts):
        texts = [f"passage: {t}" for t in texts]
        # Chroma expects a list of floats per document
        return self.model.encode(texts, convert_to_numpy=True).tolist()

    def embed_query(self, text):
        text = f"query: {text}"
        # And a list of floats for a single query
        return self.model.encode(text, convert_to_numpy=True).tolist()

if __name__ == "__main__":
    # test llm
    # print(llm.invoke("What is LangChain?"))

    # test embeddings
    emb = SentenceTransformerEmbeddings()
    print(emb.embed_query("What is LangChain?"))
