from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Load database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine and session factory
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


if __name__ == "__main__":
    # Test the database connection
    try:
        with engine.connect() as connection:
            print(engine.connect())
            print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")