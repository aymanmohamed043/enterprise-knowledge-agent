from fastapi import FastAPI

app = FastAPI(title="Enterprise Knowledge Agent API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Enterprise Knowledge Agent API!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}