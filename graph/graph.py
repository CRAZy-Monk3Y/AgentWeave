from langgraph.graph import StateGraph
from graph.nodes import start_node, weather_node, rag_node
from graph.router import route_question
from typing import List, TypedDict
from langfuse.langchain import CallbackHandler

langfuse_handler = CallbackHandler()


class GraphState(TypedDict, total=False):
    question: str
    answer: str
    sources: List[str]
    chunks: List[str]

def build_graph():
    graph = StateGraph(GraphState)

    # Nodes
    graph.add_node("start", start_node)
    graph.add_node("weather", weather_node)
    graph.add_node("rag", rag_node)

    # Conditional routing
    graph.add_conditional_edges(
        "start", route_question, {"weather": "weather", "rag": "rag"}
    )

    graph.set_entry_point("start")

    return graph.compile().with_config({"callbacks": [langfuse_handler]})
