from pathlib import Path
import sys
import logging

# Ensure the repo root is on sys.path so absolute imports work
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from backend.app.agents.state import AgentState
from backend.app.agents.orchestrator import orchestrator_node
from backend.app.agents.tool_node import query_db, search_docs
from backend.app.agents.formatter import formatter_node
from backend.app.agents.refiner import refiner_node

logger = logging.getLogger(__name__)

# Prebuild the tool node so we can wrap it with logging
all_tools = [query_db, search_docs]
_tool_node = ToolNode(all_tools)


def _action_layer_node(state: AgentState) -> dict:
    """Runs tools and logs the result for graph node tracing."""
    out = _tool_node.invoke(state)
    messages = out.get("messages", [])
    for i, msg in enumerate(messages):
        content = getattr(msg, "content", str(msg))[:500]
        name = getattr(msg, "name", "tool")
        logger.info(
            "graph node=action_layer | tool_message=%s | name=%s | content_preview=%s",
            i + 1,
            name,
            content[:200] + "..." if len(str(content)) > 200 else content,
        )
    return out


# 1. Initialize the State Machine
workflow = StateGraph(AgentState)

# 2. Add the "Brain" (The Orchestrator)
workflow.add_node("orchestrator", orchestrator_node)
workflow.add_node("formatter", formatter_node)
workflow.add_node("refiner", refiner_node)

# 3. Add the "Hands" (The Action Layer) with logging
workflow.add_node("action_layer", _action_layer_node)

# 4. Set the Entry Point
workflow.set_entry_point("refiner")
workflow.add_edge("refiner", "orchestrator")

# 5. Define the "Conditional Edge" (The Traffic Controller)
workflow.add_conditional_edges(
    "orchestrator",
    tools_condition,
    {
        "tools": "action_layer", # Map the 'tools' signal to our node name
        "__end__": "formatter"           # Map the 'finish' signal to the end of the graph
    }
)

# 6. The Feedback Loop
workflow.add_edge("action_layer", "formatter")
workflow.add_edge("formatter", END)
# 7. Final Compilation
# This creates the 'app_graph' object that we will import into FastAPI.
app_graph = workflow.compile()

if __name__ == "__main__":

    def run_test(query: str, role: str):
        print(f"\n--- 🚀 TESTING ROLE: {role.upper()} ---")
        print(f"User Query: {query}")
        
        # Initialize the briefcase (State)
        inputs = {
            "messages": [HumanMessage(content=query)],
            "user_role": role
        }
        
        # Run the graph! 
        # 'config' with 'recursion_limit' prevents infinite loops
        config = {"recursion_limit": 10}
        
        # .stream() allows us to see exactly which node is working
        for output in app_graph.stream(inputs, config=config):
            for key, value in output.items():
                print(f"\n📍 Node Working: {key}")
                # Optional: print the last message content to see the 'thought'
                if "messages" in value:
                    last_msg = value["messages"][-1]
                    print(f"Content: {last_msg.content[:200]}...")

        # Final Result
        # We grab the very last state after the graph finishes
        final_state = app_graph.invoke(inputs)
        print("\n✅ FINAL ANSWER:")
        print(final_state["messages"][-1].content)
        print("-" * 40)
    
    # Test 1: Admin asking for SQL data (Should use query_business_data)
    run_test("give me all roles?", "admin")
    
    # Test 2: HR asking for SQL data (Should be BLOCKED/Refused)
    # run_test("Tell me the salary of the CEO", "hr")
    
    # Test 3: HR asking for policies (Should use query_knowledge_base)
    # run_test("What is the company policy on remote work?", "hr")


