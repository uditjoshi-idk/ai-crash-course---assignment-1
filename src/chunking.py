from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
    "BAAI/bge-large-en"
)

def chunk_text(text: str, chunk_size: int = 512, overlap: int = 100):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")
    if overlap < 0:
        raise ValueError("overlap must be non-negative")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    tokens = tokenizer.encode(
        text,
        add_special_tokens=False
    )

    chunks = []

    start = 0
    while start < len(tokens):
        end = start + chunk_size

        chunk_tokens = tokens[start:end]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append(chunk_text)
        start += chunk_size - overlap

    return chunks
