from app.database.executor import execute_query

query = """
SELECT
    SUM(booking_amount) AS total_booking
FROM actual_booking_invoices_collection;
"""

result = execute_query(query)

print(result)