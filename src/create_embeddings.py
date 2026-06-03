import pandas as pd
from sentence_transformers import SentenceTransformer
from chunking import chunk_text

def create_embeddings_with_csv(
    data_path,
    output_csv="product_embeddings.csv",
    limit=5000,
    model_name="BAAI/bge-large-en"):

    df = pd.read_excel(data_path).head(limit)
    rows = []
    texts = []

    for idx, row in df.iterrows():
        description = (str(row["description"]) if pd.notna(row["description"]) else "")
        specs = (str(row["specifications_text"]) if pd.notna(row["specifications_text"]) else "")

        combined_text = (
            f"Product Name: {row['name']}\n"
            f"Description: {description}\n"
            f"Specifications: {specs}"
        )

        chunks = chunk_text(
            combined_text,
            chunk_size=512,
            overlap=100
        )

        for chunk_idx, chunk in enumerate(chunks):
            texts.append(chunk)

            rows.append({
                "product_id": str(idx),
                "chunk_id": chunk_idx,
                "name": row["name"],
                "document": chunk
            })

    model = SentenceTransformer(model_name)
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
    )

    for i, emb in enumerate(embeddings):
        rows[i]["embedding"] = emb.tolist()

    export_df = pd.DataFrame(rows)

    export_df.to_csv(output_csv, index=False)

    return export_df