""" only send last message to the model """

from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.messages import RemoveMessage


load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

messages = [AIMessage(f"So you said you were searching ocean mammals?", name="Bot")]

messages.append(HumanMessage(f"Yes, I know about whales. But what others should I learn about?", name="Aniket"))
messages.append(AIMessage(f"Message 2", name="Aniket"))
messages.append(HumanMessage(f"Message 2 human response", name="Aniket"))

# for m in messages:
#     m.pretty_print()
# result = llm.invoke(message)
# print(result)

# Nodes

def chat_model_node(state: MessagesState):
    return {"messages": llm.invoke(state['messages'][-1:])}


# Build graph
builder = StateGraph(MessagesState)
builder.add_node("chat_model", chat_model_node)
builder.add_edge(START, "chat_model")
builder.add_edge("chat_model", END)


graph = builder.compile()

# View


print(graph.get_graph().draw_mermaid())
graph.get_graph().print_ascii()

output = graph.invoke({'messages': messages})