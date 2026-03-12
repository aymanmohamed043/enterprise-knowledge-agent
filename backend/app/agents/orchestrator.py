from pathlib import Path
import sys
import logging

# Ensure the repo root is on sys.path so absolute imports work
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from langchain_core.messages import SystemMessage, HumanMessage
from sqlalchemy.orm import Session
from backend.app.agents.tool_node import get_tools_for_role
from backend.app.agents.state import AgentState
from backend.app.core.llm import llm
from backend.app.agents.prompts import ADMIN_PROMPT, ANALYST_PROMPT, HR_PROMPT
from backend.app.tools.schema_helper import get_database_schema
from backend.app.tools.vector_db import get_vector_store
from backend.app.db.database import SessionLocal

from backend.app.tools.vector_db_helper import get_knowledge_catalog
logger = logging.getLogger(__name__)


def orchestrator_node(state: AgentState):
    role = state.get("user_role", "viewer")

    # Create a temporary session to fetch metadata
    db = SessionLocal() 
    try:
        # 1. Get the Schema (So the Analyst/Admin knows the table names!)
        schema_info = get_database_schema()
        # 2. Get the Vector Database Metadata (using the temporary session)
        vector_db_metadata = get_knowledge_catalog(db) 
    finally:
        db.close() # Close the session after use

    allowed_tools = get_tools_for_role(role)
    # print(f"allowed_tools: {allowed_tools}")

    # 2. Select the right Persona
    if role == "admin":
        persona = ADMIN_PROMPT.format(schema=schema_info, allowed_tools=allowed_tools, vector_db_metadata=vector_db_metadata)
    elif role == "analyst":
        persona = ANALYST_PROMPT.format(schema=schema_info, allowed_tools=allowed_tools)
    elif role == "hr":
        persona = HR_PROMPT.format(allowed_tools=allowed_tools, vector_db_metadata=vector_db_metadata)
    else:
        persona = "You are a viewer with no tool access. Answer general questions only."

    # 3. Bind tools based on role (Security Layer)
    model_with_tools = llm.bind_tools(allowed_tools)

    input_message = [SystemMessage(content=persona)] + state["messages"]
    logger.info(f"input message in orchestrator node: {input_message} ")

    response = model_with_tools.invoke(input_message)

    # Log orchestrator result for each node trace
    tool_calls = getattr(response, "tool_calls", None) or []
    content_preview = ""
    if hasattr(response, "content") and response.content:
        raw = response.content
        if isinstance(raw, str):
            content_preview = raw[:300] + "..." if len(raw) > 300 else raw
        else:
            content_preview = str(raw)[:300]
    
    return {"messages": [response]}

if __name__ == "__main__":
    # test orchestrator_node
    message_content = "give me all users in the system"
    state = AgentState(messages=[HumanMessage(content=message_content)], user_role="hr")
    print(orchestrator_node(state))