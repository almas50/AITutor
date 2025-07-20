import os
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

persist_directory = "rag/chroma_db"

embeddings = OpenAIEmbeddings()

db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

def retrieve_context(user_message: str, k: int = 2) -> str:
    results = db.similarity_search(user_message, k=k)
    if not results:
        return ""

    context_parts = [doc.page_content for doc in results]
    return "\n\n".join(context_parts)