from typing import TypedDict, Annotated
from langgraph.graph import START, END, StateGraph


def reduce_list(left : list | None, right : list | None) -> list:
    """Here we are trying to safely combine two list.
        Let's say you are trying to cobile none with list in that case you would get error.
        So, In such conditions you can use custome reducer.
    """
    if not left:
        left = [0]
    if not right:
        right = [0]
    return left + right

class CustomeReducerState(TypedDict):
    foo : Annotated[list[int], reduce_list]

def node_1(state):
    print("---node_1---")
    return {'foo' : [state['foo'][0] + 1]}

def node_2(state):
    print("---node_2---")
    return {'foo' : [state['foo'][0] + 2]}

def node_3(state):
    print("---node_3---")
    return {'foo' : [state['foo'][0] + 3]}

builder = StateGraph(CustomeReducerState)

builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)


builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_1", "node_3")
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

graph = builder.compile()

result = graph.invoke({'foo' : None})

print(result)
    