# rag/vectorstore.py
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from langchain_qdrant import QdrantVectorStore
from rag.embeddings import get_embeddings

COLLECTION_NAME = "pdf_rag_collection"
QDRANT_URL = "http://localhost:6431"


def get_client():
    return QdrantClient(url=QDRANT_URL)


def ensure_collection(embedding_dim: int):
    client = get_client()
    collections = [c.name for c in client.get_collections().collections]

    if COLLECTION_NAME in collections:
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=embedding_dim,
            distance=Distance.COSINE,
        ),
    )


def create_vectorstore(chunks):
    embeddings = get_embeddings()

    ensure_collection(768)

    client = get_client()

    vectorstore = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings, 
    )

    vectorstore.add_documents(chunks)
    return vectorstore


def load_vectorstore():
    embeddings = get_embeddings()
    client = get_client()

    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,  
    )
