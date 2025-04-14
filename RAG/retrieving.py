import os
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

# Define persistent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
persistent_dir = os.path.join(current_dir, "db", "chroma_db")


# Define the embedding model
model_name = "BAAI/bge-small-en"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}

embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)


# Load the existing vector store with the embedding function
db = Chroma(persist_directory=persistent_dir, embedding_function=embeddings)

# Define the user's question
query = "Can I get any discount?"

retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs = {"k":3, "score_threshold": 0.5},
)

relevent_docs = retriever.invoke(query)


# Display the relevent results with metadata
print(("\n--- Relevent Documents"))
for i, doc in enumerate(relevent_docs, 1):
    print(f"Document {i}: \n{doc.page_content}\n")
    if doc.metadata:
        print(f"Source: {doc.metadata.get('source', 'Unknown')}\n")