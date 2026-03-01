from pathlib import Path
import sys

# Ensure the repo root is on sys.path so absolute imports work
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from sqlalchemy import inspect
from backend.app.db.database import engine 

def get_database_schema():
    """
    Scans the PostgreSQL database and returns a string 
    describing all tables and columns.
    """
    # 1. Initialize the Inspector
    # This is a SQLAlchemy tool that "looks inside"  DB.
    inspector = inspect(engine)
    
    # 2. Get all table names
    table_names = inspector.get_table_names()
    
    schema_description = "### DATABASE SCHEMA ###\n\n"
    
    for table_name in table_names:
        # Security Note: We skip 'access_logs' so the AI doesn't 
        # get distracted by internal audit tables.
        if table_name == "access_logs":
            continue
            
        schema_description += f"Table: {table_name}\n"
        
        # 3. Get columns for this table
        columns = inspector.get_columns(table_name)
        for column in columns:
            col_name = column['name']
            col_type = str(column['type'])
            schema_description += f" - {col_name} ({col_type})\n"
        
        schema_description += "\n"
    
    return schema_description

# Simple test to see what the AI will see
if __name__ == "__main__":
    print(get_database_schema())