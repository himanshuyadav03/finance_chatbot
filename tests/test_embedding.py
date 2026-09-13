from app.rag.embedding_service import create_embedding


text = """
Table: actual_booking_invoices_collection
Column: booking_amount
Details: Actual booking amount
"""


embedding = create_embedding(text)


print("Embedding type:", type(embedding))
print("Embedding length:", len(embedding))
print("First 10 values:", embedding[:10])