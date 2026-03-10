import os
import time
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. Setup Logging for observability
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 2. Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# 3. Resilient Engine Factory
def get_engine_with_retry(url, max_retries=5, delay=2):
    """
    Attempts to connect to the database. If it fails (common in Docker 
    during startup), it retries before crashing.
    """
    attempt = 0
    while attempt < max_retries:
        try:
            # Create the engine
            engine = create_engine(url)
            # Verifying the connection immediately
            with engine.connect() as connection:
                logger.info("✅ Database connection established successfully!")
                return engine
        except exc.OperationalError:
            attempt += 1
            logger.warning(
                f"⚠️ Database not ready yet. Attempt {attempt}/{max_retries}. "
                f"Retrying in {delay}s..."
            )
            time.sleep(delay)
    
    logger.error("❌ Failed to connect to the database after maximum retries.")
    raise ConnectionError("Database connection failed. Is the container running?")

# 4. Initialize Core Components
engine = get_engine_with_retry(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 5. FastAPI Dependency
def get_db():
    """
    Dependency that creates a new SQLAlchemy Session for each request.
    Closes the session once the request is complete.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    # Test block for local verification
    try:
        with engine.connect() as connection:
            print("Status: Operational")
    except Exception as e:
        print(f"Status: Failed - {e}")