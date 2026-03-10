import sys
import os
import uvicorn

if __name__ == "__main__":
    # 1. Get the absolute path to the 'backend' folder
    backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
    
    # 2. Add it to Python's "Search Path"
    # This tells Python: "If I ask for 'app', look inside the 'backend' folder"
    sys.path.append(backend_path)

    # 3. Start the Server
    print(f"🚀 Starting Server. Added to path: {backend_path}")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)