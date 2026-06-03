import chromadb
from sentence_transformers import SentenceTransformer


def get_top_k(query: str, model, collection_name: str = "product_collection_assignment_2", db_path: str = "./chroma_db", k: int = 5):
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_collection(name=collection_name)

    query_embedding = model.encode([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
    )
    return results
