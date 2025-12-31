from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.types import interrupt
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
import uuid

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

class State(TypedDict):
    query: str
    ai_answer: str
    human_feedback: str


def ai_node(state: State):
    response = llm.invoke(state["query"])
    return {"ai_answer": response.content}


def human_review_node(state: State):
    feedback = interrupt({
        "ai_answer": state["ai_answer"],
        "instruction": "Review the answer. Approve or edit it."
    })
    return {"human_feedback": feedback}


def route_after_human(state: State):
    if "reject" in state["human_feedback"].lower():
        return "ai"
    return "final"


def final_node(state: State):
    return {
        "final_answer": state["human_feedback"]
        if state["human_feedback"]
        else state["ai_answer"]
    }


graph = StateGraph(State)
graph.add_node("ai", ai_node)
graph.add_node("human_review", human_review_node)
graph.add_node("final", final_node)

graph.set_entry_point("ai")
graph.add_edge("ai", "human_review")
graph.add_conditional_edges("human_review", route_after_human)
graph.add_edge("final", END)

checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

thread_id = str(uuid.uuid4())

# ⏸️ First call — pause
result = app.invoke(
    {"query": "Explain RAG in simple terms"},
    config={"configurable": {"thread_id": thread_id}}
)
print(result)

# ▶️ Second call — resume
result = app.invoke(
    {"human_feedback": "Approved. Looks good."},
    config={"configurable": {"thread_id": thread_id}}
)
print(result)
