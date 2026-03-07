import os
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from dotenv import load_dotenv
load_dotenv(_REPO_ROOT / "backend" / ".env")

import json
from mistralai import Mistral

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

async def generate_document_metadata(context_text: str):
    """
    Uses Mistral to analyze document text and extract metadata.
    """
    context_text = context_text[:10000] if len(context_text) > 10000 else context_text # limit the context text to 10000 tokens 
    prompt = f"""
        Analyze the provided document text and generate a structured JSON extraction.

        CONSTRAINTS:
        1. SUMMARY: One powerful sentence starting with the document type and its exact purpose (e.g., "Technical Manual for X...").
        2. KEYWORDS: Extract 3 bullet points summarizing the most critical info for a decision-maker.

        TEXT:
        {context_text}

        RETURN ONLY VALID JSON:
        {{
            "summary": "The single identifying sentence...",
            "keywords": "point 1, point 2, point 3" 
        }}
    """
    # prompt is already filled via f-string above; do not call .format() or braces like {"summary"} become placeholders and cause KeyError

    if not MISTRAL_API_KEY:
        print("AI Librarian Error: MISTRAL_API_KEY not set. Add it to backend/.env")
        return {"summary": "Summary unavailable.", "keywords": "document"}

    try:
        client = Mistral(api_key=MISTRAL_API_KEY)
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {"role": "system", "content": "You are a professional document auditor. Extract data with 100% accuracy. Output only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        clean_content = response.choices[0].message.content.strip()
        data = json.loads(clean_content)
        return {
            "summary": data.get("summary", "Summary unavailable."),
            "keywords": data.get("keywords", "document"),
        }
    except Exception as e:
        print(f"AI Librarian Error: {e}")
        return {
            "summary": "Summary unavailable.",
            "keywords": "document"
        }

if __name__ == "__main__":
    context_text = """
        Here is a very long, detailed text about LangGraph, structured to be comprehensive and informative. It covers its core concepts, architecture, key features, and practical applications.

        ---

        ### LangGraph: Orchestrating Complex AI Workflows with Cyclic Graphs

        In the rapidly evolving landscape of Large Language Models (LLMs), the ability to chain together calls, tools, and external data sources has become paramount. While early frameworks like LangChain provided the building blocks for linear "chains" of operations, the next generation of AI applications demands more flexibility, statefulness, and control. Enter **LangGraph**, a revolutionary library built on top of LangChain that reimagines agentic workflows not as simple sequences, but as **cyclic graphs**.

        LangGraph is an orchestration framework designed to model agent and multi-agent workflows as graphs. By moving beyond the constraints of directed acyclic graphs (DAGs) commonly found in other orchestration tools, LangGraph introduces cycles, the single most critical feature for building truly autonomous, reflective, and adaptive agents. This text provides a deep dive into LangGraph, exploring its philosophy, core components, architectural patterns, and the transformative potential it holds for the future of AI.

        #### The Genesis: From Chains to Cycles

        To understand LangGraph, it's essential to understand the limitations of its predecessor's most common paradigms. LangChain popularized the concept of chains—predefined sequences of LLM calls and tools. For example, a chain might: 1) Take a user question, 2) Retrieve relevant documents from a vector store, 3) Feed the question and documents to an LLM, and 4) Return an answer. This is a powerful and effective pattern for many applications, represented as a directed acyclic graph (DAG) where data flows in one direction without loops.

        However, truly intelligent agents are rarely so linear. An agent might need to:
        - **Reflect:** Execute a plan, observe the result, and then refine its next action based on that observation.
        - **Use Tools Dynamically:** Decide to call a web search, analyze the results, and then realize it needs to call a calculator or a database query before formulating a final answer.
        - **Engage in Multi-Agent Collaboration:** Have a "researcher" agent gather information and pass its findings to a "writer" agent, which might then ask the researcher for clarification, creating a feedback loop.

        These scenarios are fundamentally cyclic. They require loops. Traditional DAG-based systems struggle to model this elegantly, often resorting to complex, hard-coded logic or "agent loops" that are external to the core orchestration model. LangGraph was born from the insight that the **graph** itself should be the executor of the loop. By incorporating cycles as a first-class citizen, LangGraph allows developers to embed the very logic of reflection and iteration directly into the structure of the workflow.

        #### Core Concepts: The Building Blocks of a Graph

        LangGraph's architecture is built on a small but powerful set of concepts that together provide immense flexibility.

        1.  **`State`:** The heart of any LangGraph application is the **State**. The state is a typed data structure (typically a TypedDict or a Pydantic model) that represents the complete snapshot of your workflow at any given moment. It is the "single source of truth." Every node in the graph reads from and writes to this shared state. This design is a departure from many other frameworks where data is passed explicitly between steps. In LangGraph, the flow of data is implicit; nodes are functions that accept the current state and return an update to it. This makes the system incredibly manageable, as the entire context of a run is always contained within one object.

        2.  **`Node`:** Nodes are the fundamental units of work. Each node is typically a Python function (or a runnable) that encapsulates a specific task. Common examples include:
            - An LLM call with a specific prompt.
            - A tool-calling function (e.g., `search_web`, `calculate`).
            - A conditional logic function (e.g., `should_continue`).
            - A human-in-the-loop interaction point.
            A node takes the current `State` as input and returns a **state update**, which is a partial dictionary containing only the keys it intends to modify.

        3.  **`Edge`:** Edges define the paths of execution between nodes. They dictate the flow of control. LangGraph has two primary types of edges:
            - **Normal Edges:** These are direct, unconditional transitions from one node to the next. After Node A finishes, the graph will always go to Node B.
            - **Conditional Edges:** This is where the power of LangGraph truly shines. A conditional edge calls a function (a "router") that analyzes the current `State` and returns the name of the next node to navigate to. This is the mechanism that enables loops, branching, and dynamic decision-making. For instance, after an LLM node, a conditional edge can check if the LLM's output contains a tool call. If it does, the graph routes to a `call_tool` node; if not, it routes to a `final_answer` node.

        4.  **`Graph`:** The graph is the container that orchestrates all the nodes and edges. You define your workflow by adding nodes and connecting them with edges. LangGraph provides different graph types, with `StateGraph` being the primary one for agentic workflows. Once defined, the graph can be compiled, which validates the structure and prepares it for execution.

        #### The Power of the Cycle: Enabling Agentic Behavior

        The introduction of cycles via conditional edges is the defining feature of LangGraph. Consider the canonical example of a ReAct agent (Reason + Act). The agent's logic is a loop:
        1.  **Reason:** LLM decides on an action (e.g., "I need to search for the weather in Paris").
        2.  **Act:** The system executes the action (calls a weather API).
        3.  **Observe:** The result of the action (the weather data) is fed back to the LLM.
        4.  **Reason Again:** The LLM processes the observation and decides the next step (e.g., "Now I can answer the user" or "I need to call another tool").

        In a DAG, you could implement steps 1, 2, and 3, but step 4 (going back to step 1) would be impossible without an external loop. In LangGraph, this is elegantly modeled:
        - You have nodes: `call_llm`, `execute_tool`.
        - You have a conditional edge from `call_llm`: if the output has a tool call, go to `execute_tool`; otherwise, go to `final`.
        - You have a normal edge from `execute_tool` back to `call_llm`.

        The graph itself is the loop. It will continue to cycle between these nodes until the conditional edge decides it's time to finish. This recursive, self-referential structure is what makes agents built with LangGraph feel truly autonomous.

        #### Key Features and Capabilities

        Beyond its core graph architecture, LangGraph boasts a suite of powerful features designed for production-grade agentic systems.

        - **Human-in-the-Loop (HIL):** For many critical applications, allowing a human to intervene is non-negotiable. LangGraph natively supports HIL by providing the ability to **interrupt** the graph at specific nodes. The system can persist its state, wait for human input, and then **resume** execution from the exact point it left off. This is crucial for scenarios like review-and-approval workflows, data labeling, or any situation requiring human judgment before proceeding.

        - **Persistence and Checkpointing:** LangGraph integrates seamlessly with LangChain's checkpointing system. The state of a graph run can be saved after every step (a "checkpoint"). This is invaluable for debugging, allowing developers to rewind and replay a run to understand its decision-making process. It also enables robust error recovery and the ability to manage long-running, persistent agents.

        - **Streaming Support:** LLM calls can be slow. LangGraph provides first-class support for streaming. You can stream not only the tokens from the final LLM call but also the intermediate steps of the graph. This allows you to build user interfaces that show the agent's "thinking" in real-time—displaying the tool calls it makes, the results it retrieves, and its internal reasoning before the final answer is formed.

        - **Multi-Agent Architectures:** LangGraph is an ideal platform for building systems composed of multiple specialized agents. You can define each agent as its own subgraph or node, and then create a "supervisor" node that manages the communication and handoffs between them. This leads to powerful patterns like:
            - **Hierarchical Teams:** A supervisor agent delegates tasks to specialist agents (e.g., a researcher, a coder, a reviewer).
            - **Collaborative Swarms:** Multiple agents work on the same problem, sharing information and passing tasks between each other in a dynamic, peer-to-peer manner.

        #### A Practical Example: A Reflective Research Agent

        Let's imagine building an advanced research agent that can generate a report and then critique and refine it. This is a classic example of a workflow that requires a cycle.

        **Goal:** Answer a complex user query by generating a report, reflecting on it, and improving it.

        **State:**
        ```python
        from typing import TypedDict, List, Annotated
        import operator

        class ResearchState(TypedDict):
            query: str
            initial_report: str
            critique: str
            revised_report: str
            iterations: int
            messages: Annotated[List[str], operator.add] # Append-only list
        ```

        **Nodes:**
        1.  **`generate_report`**: Takes the `query` from the state and uses an LLM to write a detailed `initial_report`. Updates the `initial_report` field.
        2.  **`critique_report`**: Takes the `initial_report` and the `query`, and uses a second LLM (or the same one with a different prompt) to act as a critic, identifying weaknesses, gaps, and areas for improvement. Updates the `critique` field.
        3.  **`revise_report`**: Takes the `initial_report`, the `critique`, and the `query`, and asks an LLM to produce a `revised_report` that addresses the critique.
        4.  **`finalize`**: A simple node that formats the `revised_report` as the final answer.

        **Conditional Logic (Router):**
        After the `revise_report` node, we have a conditional edge that calls a function `should_continue`. This function checks the `iterations` count in the state. If `iterations < 2`, it increments the count and routes back to the `critique_report` node for another round of improvement. If `iterations >= 2`, it routes to the `finalize` node.

        **Graph Construction:**
        - Start Node: `generate_report`
        - Edge: `generate_report` -> `critique_report`
        - Edge: `critique_report` -> `revise_report`
        - Conditional Edge: `revise_report` -> `should_continue` (routes back to `critique_report` or to `finalize`)
        - Edge: `finalize` -> END

        This simple graph demonstrates a powerful, self-improving loop. The agent doesn't just produce an answer; it reflects on its own output and iteratively refines it based on a simulated "critic." This is a level of sophistication that is natural to build in LangGraph but cumbersome in linear frameworks.

        #### The Future of Orchestration

        LangGraph represents a significant maturation in the field of AI application development. It moves the metaphor from a simple assembly line (chains) to a dynamic, intelligent organism (a cyclic graph). By embracing concepts from computer science like state machines and graph theory, it provides a robust and scalable foundation for building the next generation of AI systems.

        As agents become more complex, moving from single tasks to multi-step projects and from solo actors to collaborative teams, the need for sophisticated orchestration will only grow. LangGraph, with its focus on cycles, state management, and human-in-the-loop, is uniquely positioned to be the operating system for this new era of agentic AI, enabling developers to build systems that are not just reactive, but truly proactive, reflective, and intelligent.
    """
    print(generate_document_metadata(context_text))

