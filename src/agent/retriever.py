from typing import List
from langchain_core.embeddings import Embeddings
from langchain_chroma import Chroma


class SentenceTransformerEmbeddings(Embeddings):
    r"""
    Adapter that wraps a SentenceTransformer model to implement
    LangChain's Embeddings interface.
    """

    def __init__(self, model):
        self.model = model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts).tolist()

    def embed_query(self, text: str) -> List[float]:
        return self.model.encode([text])[0].tolist()


class ChromaRetriever:
    r"""
    This class is responsible for retrieving the top-k relevant products
    from the ChromaDB vector database based on semantic similarity to the user query.
    Uses LangChain's Chroma vector store wrapper.
    """
    def __init__(self, model, db_path="./chroma_db", collection_name="product_collection_assignment_2", k=5):
        self.k = k
        self.embeddings = SentenceTransformerEmbeddings(model)
        self.vectorstore = Chroma(
            collection_name=collection_name,
            persist_directory=db_path,
            embedding_function=self.embeddings,
        )

    def retrieve(self, user_query: str):
        r"""
        Retrieve the top-k most similar documents to the user query.
        Returns results in the same dict format as raw ChromaDB
        (with 'documents', 'metadatas', 'ids' keys) for backward compatibility.
        """
        results = self.vectorstore._collection.query(
            query_embeddings=[self.embeddings.embed_query(user_query)],
            n_results=self.k,
        )
        return results
