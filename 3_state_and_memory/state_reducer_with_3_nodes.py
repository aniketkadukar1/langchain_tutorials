from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    foo : Annotated[list[int] , add]

def node_1(state):
    print("---node_1---")
    return {'foo' : [state['foo'][0] + 1]}

def node_2(state):
    print("---node_2---")
    return {'foo' : [state['foo'][0] + 2]}

def node_3(state):
    print("---node_3---")
    return {'foo' : [state['foo'][0] + 3]}

builder = StateGraph(State)

builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)


builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_1", "node_3")
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

graph = builder.compile()

result = graph.invoke({'foo' : [3]})

print(result)