from langchain_pinecone import PineconeVectorStore
from app.ai.embeddings import get_embedding_function
from app.config import settings

embedding_function=get_embedding_function()

def get_vectorstore() -> PineconeVectorStore:
    return PineconeVectorStore(
        index_name=settings.TRIP_INDEX,
        embedding=embedding_function,
        pinecone_api_key=settings.PINECONE_API,
        namespace="aaa"
    )
