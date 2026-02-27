from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create the connection engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def execute_sql_query(query: str):
    """
    Executes a read-only SQL query and returns the results.
    """
    # Security: rudimentary check to prevent deletions
    if "DROP" in query.upper() or "DELETE" in query.upper() or "INSERT" in query.upper():
        return "Error: You are only allowed to READ data (SELECT)."

    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            # Convert rows to a list of dicts (JSON-like)
            keys = result.keys()
            return [dict(zip(keys, row)) for row in result.fetchall()]
    except Exception as e:
        return f"Database Error: {str(e)}"
    
    if __name__ == "__main__":
        # Test the database connection
        try:
            with engine.connect() as connection:
                print("Database connection successful!")
        except Exception as e:
            print(f"Database connection failed: {e}")
        # Test the database using query 
        query = "SELECT * FROM users;"
        print(f"query is: {query}")
        results = execute_sql_query(query)
        print(results)