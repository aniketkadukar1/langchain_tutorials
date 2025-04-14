from langchain_groq import ChatGroq
from retrieving import relevent_docs, query
from langchain_core.messages import SystemMessage, HumanMessage

combined_input = (
    "Here are some document that minght help answer the question:"
    + "is there any discount?"
    + "\n\n".join([doc.page_content for doc in relevent_docs])
    + "\n\nPlease provide a rough answer based only on the provided documents. If the answer is not found in the documents, respon with 'I'm not sure.'"    
)

# Create a Groq Model 
model = ChatGroq(model="qwen-2.5-32b", temperature=0.2)

messages = [
    SystemMessage(content="You are a helpful assistant"),
    HumanMessage(content=combined_input)
]

# Invoke the model with the combined output
result = model.invoke(messages)

# Dispaly the result with the content only
print("\n--- Generated Response ---")
print(result.content)