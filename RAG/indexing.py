from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from langchain_community.embeddings import HuggingFaceBgeEmbeddings

model_name = "BAAI/bge-small-en"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}



current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir,"documents", "membership_info.txt")
parsistent_dir = os.path.join(current_dir, "db", "chroma_db")

if not os.path.exists(parsistent_dir):
    print("Persistent directory does not exist, initializing vectore store...")

    # Ensure the text file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    # Load the text file
    loader = TextLoader(file_path)
    documents = loader.load()

    # Split the documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=5)
    docs = text_splitter.split_documents(documents)

    # Display information about the split documents
    print(f"Split {len(documents)} documents into {len(docs)} chunks")
    print("First chunk:")
    print(docs[0].page_content)

    # creating embeddings
    print("...........Creating embeddings..........")

    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)
    print("...........Finished creating embeddings..........")


    print("...........Creating vector store..........")
    db = Chroma.from_documents(docs, embeddings, persist_directory=parsistent_dir)
    print("...........Finished creating vector store..........")

else:
    print("..........Vector store already exists..........")







# load_dotenv()


# llm = ChatGroq(
#     model_name="llama3-8b-8192",
#     temperature=0.5,
# )

# result = llm.invoke("Hello, how are you? Answer in one word")
# print(result)



# from langchain_openai import OpenAIEmbeddings

# embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# from langchain_core.vectorstores import InMemoryVectorStore

# vector_store = InMemoryVectorStore(embeddings)
