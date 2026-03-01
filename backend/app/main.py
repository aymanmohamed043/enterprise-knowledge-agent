import sys
import os
from pathlib import Path
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from fastapi import FastAPI
from pydantic import BaseModel
from backend.app.core.logging_config import configure_logging
from backend.app.routers import ingest, chat

configure_logging(level=os.getenv("LOG_LEVEL", "INFO"))
app = FastAPI(title="Enterprise Knowledge Agent")

# Register the new ingestion router
app.include_router(ingest.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")

class HealthCheck(BaseModel):
    status: str = "OK"

@app.get("/", response_model=HealthCheck)
def health_check():
    return {"status": "System is running. Agents are asleep."}



if __name__ == "__main__":
    import uvicorn
    # Run on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)