from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

    user_role: str


if __name__ == "__main__":
    # test AgentState
    state = AgentState(messages=["first message", "second message"], user_role="admin")
    state["messages"].append("third message")
    print(state)