from app.rag.retriever import retrieve_metadata


question = "What percentage of booking gets invoiced within 3 weeks?"

documents = retrieve_metadata(
    question=question,
    top_k=5
)

print("Question:")
print(question)

print("\nRetrieved documents:\n")

for i, document in enumerate(
    documents,
    start=1
):
    print("=" * 60)
    print(f"Result {i}")
    print(document)