from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from qdrant_client.models import Distance, VectorParams
from rag.embeddings import get_embeddings

QDRANT_URL = "http://localhost:6431"
COLLECTION_VECTOR_SIZE = 768 

client = QdrantClient(url=QDRANT_URL)


def create_collection_if_not_exists(collection_name: str):
    existing = [c.name for c in client.get_collections().collections]

    if collection_name not in existing:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=COLLECTION_VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )


def create_vectorstore(chunks, collection_name: str):
    embeddings = get_embeddings()

    create_collection_if_not_exists(collection_name)

    vectorstore = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings
    )

    vectorstore.add_documents(chunks)

    return vectorstore


def load_vectorstore(collection_name: str):
    embeddings = get_embeddings()

    return QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings
    )
