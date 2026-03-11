import sys
from pathlib import Path
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.app.core.logging_config import configure_logging
from backend.app.routers import ingest, chat, auth
from backend.app.routers import rag_endpoint

configure_logging()
app = FastAPI(title="Enterprise Knowledge Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(ingest.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(rag_endpoint.router, prefix="/api/v1")

class HealthCheck(BaseModel):
    status: str = "OK"

@app.get("/", response_model=HealthCheck)
def health_check():
    return {"status": "System is running. Agents are asleep."}



if __name__ == "__main__":
    import uvicorn
    # Run on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)