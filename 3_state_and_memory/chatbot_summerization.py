from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, RemoveMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.memory import MemorySaver


load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-1.5-pro")


class State(MessagesState):
    summary: str


def call_model(state: State):
    summary = state.get("summary", "")

    if summary:
        system_message = f"Summary of conversation earlier: {summary}"

        messages = [SystemMessage(content=system_message)] + state["messages"]
    
    else:
        messages = state["messages"]
    
    response = model.invoke(messages)
    return {"messages" : response}

def summerize_conversation(state: State):
    
    summary = state.get("summary", "")

    if summary:
        
        summary_message = (
            f"This is a summary of conversation to date: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )
    
    else:
        summary_message = "Create a summary of the conversation above:"

    # Add prompt to our history
    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)

    # Delete all but the 2 most recent messages
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"summary": response.content, "messages": delete_messages}

def should_continue(state: State):
    """ Return the next node to execute """

    messages = state["messages"]

    # If there are more than six messages, then we summarize the conversation
    if len(messages) > 6:
        return "summarize_conversation"
    
    return END


# Define a new graph
workflow = StateGraph(State)
workflow.add_node("conversation", call_model)
workflow.add_node(summerize_conversation)

# set the entrypoint as conversation
workflow.add_edge(START, "coversation")
workflow.add_conditional_edges("conversation", should_continue)
workflow.add_edge("summerize_conversation", END)

# Compile
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)


# Create a thread
config = {"configurable": {"thread_id": "1"}}

# Start conversation
input_message = HumanMessage(content="Hi! I am Aniket..")
output = graph.invoke({"messages": [input_message]}, config)
