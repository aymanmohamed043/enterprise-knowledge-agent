from pathlib import Path
import sys
import os

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from dotenv import load_dotenv
load_dotenv(_REPO_ROOT / "backend" / ".env")

from langchain_core.messages import HumanMessage, AIMessage
from backend.app.agents.prompts import FORMATTER_PROMPT
from mistralai import Mistral
import logging

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

logger = logging.getLogger(__name__)

def formatter_node(state):
    role = state.get("user_role", "viewer")
    logger.info(f"state in beginning of formatter node: {state} ")    
    # Get the last message (which usually contains the tool output)
    last_tool_message = state["messages"][-1]
    raw_data = last_tool_message.content
    logger.info(f"last tool message in formatter node: {last_tool_message} ")

    # Get the orchestrator AI message (which contains the tool metadata)
    orchestrator_ai_message = state["messages"][-2]
    tool_metadata = {
        "content": orchestrator_ai_message.content,
        "tool_calls": getattr(orchestrator_ai_message, "tool_calls", []),
        "additional_kwargs": getattr(orchestrator_ai_message, "additional_kwargs", {})
    }
    logger.info(f"tool metadata in formatter node: {tool_metadata} ")

    # Get the query from the last human message
    query = "Unknown Query"
    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage):
            query = msg.content
            break

    logger.info(f"query in formatter node: {query} ")

    
    # Prepare the prompt with the raw data
    formatted_system_prompt = FORMATTER_PROMPT.format(
        role=role,
        query=query,
        tool_metadata=str(tool_metadata),
        raw_data=raw_data
    )
    
    logger.info(f"formatted system prompt in formatter node: {formatted_system_prompt} ")

    # Use Mistral for formatting (instead of Gemini)
    if not MISTRAL_API_KEY:
        logger.warning("MISTRAL_API_KEY not set; formatter will return a placeholder.")
        response = AIMessage(content="[Formatter unavailable: MISTRAL_API_KEY not set.]")
    else:
        client = Mistral(api_key=MISTRAL_API_KEY)
        mistral_response = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {"role": "system", "content": formatted_system_prompt},
                {"role": "user", "content": "Process and format the provided metadata and results."},
            ],
        )
        content = mistral_response.choices[0].message.content or ""
        response = AIMessage(content=content)

    return {"messages": [response]}