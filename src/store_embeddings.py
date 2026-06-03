import ast
from pathlib import Path

import chromadb
import pandas as pd


def _sanitize_metadata_value(value):
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return value


def store_embeddings(
    data_path: str | Path,
    collection_name: str = "product_collection_assignment_2",
    db_path: str | Path = "./chroma_db",
    batch_size: int = 1000,
    reset_collection: bool = True,
):
    if batch_size <= 0:
        raise ValueError("batch_size must be a positive integer")

    df = pd.read_csv(data_path)
    client = chromadb.PersistentClient(path=db_path)

    if reset_collection:
        try:
            client.delete_collection(collection_name)
        except Exception:
            pass

    collection = client.get_or_create_collection(name=collection_name)

    df["embedding"] = df["embedding"].apply(ast.literal_eval)
    ids = [f"{row['product_id']}_{row['chunk_id']}" for _, row in df.iterrows()]
    embeddings = df["embedding"].tolist()
    documents = df["document"].astype(str).tolist()
    metadatas = []
    for _, row in df.iterrows():
        description_value = row.get("description")
        if description_value is None or (isinstance(description_value, float) and pd.isna(description_value)):
            description_value = row.get("document")

        metadatas.append(
            {
                "name": _sanitize_metadata_value(row.get("name")),
                "description": _sanitize_metadata_value(description_value),
            }
        )
    for start in range(0, len(df), batch_size):
        end = start + batch_size
        collection.add(
            ids=ids[start:end],
            embeddings=embeddings[start:end],
            documents=documents[start:end],
            metadatas=metadatas[start:end],
        )
