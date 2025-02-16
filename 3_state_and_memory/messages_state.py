from langgraph.graph import MessagesState
from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, HumanMessage, RemoveMessage


# define a custome typeddict that includes the list of messages with add_messages reduces
class CustomeMessagesState(TypedDict):
    messages : Annotated[AnyMessage, add_messages]
    # we can add further state along with messages...
    added_key_1: str
    added_key_2: str


# Use MessagesState, that includes messages and add_message reducer already
class ExtendedMessagesState(MessagesState):
    # No need to mention 'messages' here
    added_key_1: str
    added_key_2: str

 
initial_message = [
    AIMessage(content="Hello, How can I help you today?", name='Model', id=1),
    HumanMessage(content="Help me with my mathematics assignment.", name='Aniket', id=2)
]

new_messages = AIMessage(content="Sure, I am always ready to help you. What specifically are you interested in?", name='Model', id=3)

add_messages(initial_message, new_messages)
print(add_messages)

# Removal - Delete messages from the messages list using ID
delete_messages = [RemoveMessage(id=m.id) for m in initial_message[:-2]]
print(delete_messages)