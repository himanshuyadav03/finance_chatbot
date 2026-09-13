import os
import pickle

import faiss
import numpy as np

from app.rag.document_builder import build_metadata_documents
from app.rag.embedding_service import create_embedding


INDEX_PATH = "rag_store/metadata.index"
DOCUMENTS_PATH = "rag_store/documents.pkl"


def build_vector_store():

    documents = build_metadata_documents()

    embeddings = []

    for document in documents:
        embedding = create_embedding(document)
        embeddings.append(embedding)

    embeddings_array = np.array(
        embeddings,
        dtype="float32"
    )

    dimension = embeddings_array.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings_array)

    os.makedirs(
        "rag_store",
        exist_ok=True
    )

    faiss.write_index(
        index,
        INDEX_PATH
    )

    with open(
        DOCUMENTS_PATH,
        "wb"
    ) as file:
        pickle.dump(
            documents,
            file
        )

    print(
        f"Stored {len(documents)} documents"
    )