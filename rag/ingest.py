from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

import os
from dotenv import load_dotenv

load_dotenv()

persist_directory = "rag/chroma_db"
embeddings = OpenAIEmbeddings()

def ingest():
    loader = TextLoader("rag/knowledge/grammar_present_simple.md", encoding="utf-8")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    db.add_documents(docs)

if __name__ == "__main__":
    ingest()
