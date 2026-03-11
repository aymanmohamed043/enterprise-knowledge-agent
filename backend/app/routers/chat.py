import os
import sys
import logging
from pathlib import Path
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.db.models import User, ChatHistory
from backend.app.core.auth import get_current_user
from backend.app.agents.graph import app_graph
from langchain_core.messages import HumanMessage, AIMessage

router = APIRouter(prefix="/chat", tags=["AI Chat"])
logger = logging.getLogger(__name__)


class ChatSendBody(BaseModel):
    message: str


def _message_content_to_str(content) -> str:
    """Normalize LangChain message content to a string for DB/API (content can be str or list of blocks)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and "text" in block:
                parts.append(block["text"])
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts) if parts else ""
    return str(content) if content is not None else ""

@router.post("/send")
async def chat_with_agent(
    body: ChatSendBody,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = current_user
    message = body.message
    user_id = user.id
    logger.info("chat request | user_id=%s", user_id)
    logger.info("user: %s | role: %s", user.name, user.role.name)
    role_name = user.role.name
    logger.info("chat request | user_id=%s | role=%s", user_id, role_name)

    # 2. Retrieve History (The Efficiency Point!)
    # We fetch the last 10 messages to give the AI context of the current conversation.
    db_history = db.query(ChatHistory).filter(ChatHistory.user_id == user_id)\
                   .order_by(ChatHistory.timestamp.asc()).limit(10).all()

    # 3. Convert DB rows to LangChain Messages
    formatted_history = []
    for entry in db_history:
        if entry.sender == "user":
            formatted_history.append(HumanMessage(content=entry.content))
        else:
            formatted_history.append(AIMessage(content=entry.content))
    
    # 4. Add the NEW message to the list
    formatted_history.append(HumanMessage(content=message))

    # 5. Invoke the Brain (pass db so orchestrator can call get_knowledge_catalog(db))
    initial_state = {
        "messages": formatted_history,
        "user_role": role_name,
        "db": db,
    }

    result = app_graph.invoke(initial_state)
    raw_content = result["messages"][-1].content
    ai_final_text = _message_content_to_str(raw_content)

    # 6. Persistence: Save the NEW exchange to the DB (content must be a string)
    user_msg = ChatHistory(user_id=user_id, role=role_name, content=message, sender="user")
    ai_msg = ChatHistory(user_id=user_id, role=role_name, content=ai_final_text, sender="ai")
    
    db.add(user_msg)
    db.add(ai_msg)
    db.commit()

    logger.debug("chat saved | user_id=%s", user_id)
    return {"response": ai_final_text, "role": role_name}