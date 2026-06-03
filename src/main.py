from pathlib import Path
from sentence_transformers import SentenceTransformer
from store_embeddings import store_embeddings
from query import get_top_k

PATH = Path(__file__).parent.parent

if __name__ == "__main__":
    data_path = PATH / 'product_embeddings.csv'
    # df = pd.read_excel(data_path)

    # client = chromadb.Client()
    # collection = client.get_or_create_collection(name="collection_assignment_2")
    model = SentenceTransformer("BAAI/bge-large-en")
    # df = df.head(5000)[['description', 'specifications_text']]
    store_embeddings(data_path=data_path, collection_name="product_collection_assignment_2", db_path="./chroma_db")
    while True:
        query = input("Enter your query: ")
        if query.lower() == 'q':
            break
        results = get_top_k(query=query, model=model, collection_name="product_collection_assignment_2", db_path="./chroma_db", k=5)
        print(len(results['ids'][0]))
        for i in range (len(results['ids'][0])):
            print(f"Result {i+1}:")
            print(f"ID: {results['ids'][0][i]}")
            print(f"Document: {results['documents'][0][i]}")
            print(f"Metadata: {results['metadatas'][0][i]}")
            print("-" * 50)
