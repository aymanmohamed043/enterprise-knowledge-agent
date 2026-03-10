# Build from repo root: docker build -f backend/Dockerfile .
FROM python:3.11-slim

WORKDIR /app

# Copy backend and install dependencies
COPY backend/requirements.txt ./backend/
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r backend/requirements.txt
    
COPY backend ./backend

# App expects project root on path so "backend.app" and _REPO_ROOT resolve
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
