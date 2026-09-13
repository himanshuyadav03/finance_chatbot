from app.rag.document_builder import build_metadata_documents


documents = build_metadata_documents()

print("Total documents:", len(documents))

print("\nFirst 5 documents:\n")

for doc in documents[:5]:
    print("=" * 50)
    print(doc)