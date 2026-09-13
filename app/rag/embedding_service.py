from app.llm.client import client

EMBEDDING_MODEL = "text-embedding-3-small"

def create_embedding(text: str) -> list[float]:

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding