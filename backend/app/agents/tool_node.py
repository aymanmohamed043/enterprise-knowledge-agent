from langchain_core.tools import tool
from pathlib import Path
import sys

# Ensure the repo root is on sys.path so absolute imports work
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from backend.app.tools.vector_db import search_documents
from backend.app.tools.sql import execute_sql_query


@tool
def search_docs(query: str) -> str:
    """
    Searches the vector database for relevant policies or documents.
    """
    return search_documents(query)

@tool
def query_db(sql: str) -> str:
    """
    Executes a SQL query and returns the result.
    """
    return execute_sql_query(sql)


def get_tools_for_role(role: str):
    """
    The Gatekeeper: Returns a list of tools based on the user's role.
    """
    permissions = {
        "admin": [search_docs, query_db],
        "hr": [search_docs],
        "analyst": [query_db],
        "viewer": []
    }
    return permissions.get(role, [])


if __name__ == "__main__":
    # test get_tools_for_role
    print(get_tools_for_role("admin"))
    print(get_tools_for_role("hr"))
    print(get_tools_for_role("analyst"))
    print(get_tools_for_role("viewer"))