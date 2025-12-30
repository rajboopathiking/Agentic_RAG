from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import MemorySaver
from tools import rag_retrieve,evaluate_confidence, State, web_search, final_answer

graph = StateGraph(State)

graph.add_node("rag", rag_retrieve)
graph.add_node("evaluate", evaluate_confidence)
graph.add_node("web", web_search)
graph.add_node("final", final_answer)

graph.add_edge(START, "rag")
graph.add_edge("rag", "evaluate")


def routing(state: State):
    return "final" if state["confidence"] > 0.6 else "web"

graph.add_conditional_edges("evaluate", routing, {
    "final": "final",
    "web": "web"
})

graph.add_edge("web", "final")
graph.add_edge("final", END)

app = graph.compile(checkpointer=MemorySaver())