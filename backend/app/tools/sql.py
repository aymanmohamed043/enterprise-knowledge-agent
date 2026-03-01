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
    # make it accept only select queries any thing elss return error
    if not query.upper().startswith("SELECT"):
        return "Error: You are only allowed to READ data (SELECT) queries."

    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            keys = list(result.keys())
            rows = [dict(zip(keys, row)) for row in result.fetchall()]
            # Return a clear string so the LLM uses exact data (no hallucinated names/values)
            if not rows:
                return "Query returned 0 rows."
            lines = [f"Row {i+1}: " + ", ".join(f"{k}={repr(v)}" for k, v in r.items()) for i, r in enumerate(rows)]
            return f"Query returned {len(rows)} row(s):\n" + "\n".join(lines)
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
    query = "SELECT u.name FROM users u JOIN roles r ON u.role_id = r.id WHERE r.name = 'viewer';"
    print(f"query is: {query}")
    results = execute_sql_query(query)
    print(results)