from typing import Annotated, TypedDict
from operator import add
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    foo : Annotated[list[int], add]

def node_1(state):
    return {'foo' : [state['foo'][0] + 1]}

builder = StateGraph(State)

builder.add_node("node_1", node_1)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

graph = builder.compile()

result = graph.invoke({'foo' : [3]})
print(result)