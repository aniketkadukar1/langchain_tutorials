from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END, START
import random

class State(TypedDict):
    graph_state: str

def node_1(state):
    print("---node_1---")
    return {'graph_state': state['graph_state'] + 'My mood is '}

def node_2(state):
    print("---node_2---")
    return {'graph_state': state['graph_state'] + 'Good!'}

def node_3(state):
    print("---node_3---")
    return {'graph_state': state['graph_state'] + 'Bad!'}


def decide_mood(state) -> Literal["node_2", "node_3"]:

    user_input = state['graph_state']

    if random.random() < 0.5:
        return "node_2"
    
    return "node_3"

# build graph
builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Logic
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

graph = builder.compile()

print(graph.invoke({'graph_state': 'My name is Aniket.'}))