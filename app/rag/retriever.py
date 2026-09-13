import pickle

import faiss
import numpy as np

from app.rag.embedding_service import create_embedding
from app.rag.vector_store import (
    INDEX_PATH,
    DOCUMENTS_PATH,
)


def retrieve_metadata(
    question: str,
    top_k: int = 5
) -> list[str]:

    # Load FAISS index
    index = faiss.read_index(
        INDEX_PATH
    )

    # Load original documents
    with open(
        DOCUMENTS_PATH,
        "rb"
    ) as file:
        documents = pickle.load(file)

    # Convert question to embedding
    question_embedding = create_embedding(
        question
    )

    question_array = np.array(
        [question_embedding],
        dtype="float32"
    )

    # Search similar documents
    distances, indices = index.search(
        question_array,
        top_k
    )

    retrieved_documents = []

    for index_value in indices[0]:

        if index_value == -1:
            continue

        retrieved_documents.append(
            documents[index_value]
        )

    return retrieved_documents