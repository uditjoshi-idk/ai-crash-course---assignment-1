import pandas as pd
from sentence_transformers import SentenceTransformer

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

        texts.append(combined_text)
        rows.append({
            "product_id": str(idx),
            "name": row["name"],
            "document": combined_text,
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