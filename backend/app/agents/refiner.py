from pathlib import Path
import sys
import logging
import os

# Ensure the repo root is on sys.path so absolute imports work
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from dotenv import load_dotenv
load_dotenv(_REPO_ROOT / "backend" / ".env")

from backend.app.agents.state import AgentState
from langchain_core.messages import SystemMessage, HumanMessage
from mistralai import Mistral

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

logger = logging.getLogger(__name__)


def refiner_node(state: AgentState):
    """
    Analyzes history to resolve pronouns (their, them, it) 
    and carrying over previous filters.
    """
    history = state["messages"][:-1]
    current_query = state["messages"][-1].content

    logger.info(f"current query in refiner node : {current_query} ")
    logger.info(f"history in refiner node : {history} ")

    if not history:
        return {"messages": state["messages"]}

    instruction = (
        "You are a query refiner. Rewrite the user's question to be standalone "
        "using the history. Resolve pronouns like 'their' or 'them'. "
        "OUTPUT ONLY THE REWRITTEN QUESTION. NO CONVERSATION."
    )
    
    context_data = f"History: {history}\nQuestion: {current_query}"

    # We use a cheaper/faster call here just to fix the string
    # will use mistral to refine the query
    client = Mistral(api_key=MISTRAL_API_KEY)
    mistral_response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": context_data},
        ],
    )
    refined_query = mistral_response.choices[0].message.content.strip()
    refined_query = refined_query.replace('"', '').replace("'", "")
    logger.info(f"refined query in refiner node : {refined_query} ")
    
    # Replace the last message with the "Perfect Query"
    new_messages = list(state["messages"])
    new_messages[-1] = HumanMessage(content=refined_query)
    
    return {"messages": new_messages}