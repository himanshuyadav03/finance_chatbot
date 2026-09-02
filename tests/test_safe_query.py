from app.services.query_service import execute_safe_query


sql = """
SELECT
    SUM(booking_amount) AS total_booking
FROM actual_booking_invoices_collection
WHERE booking_week BETWEEN '2025Wk01' AND '2025Wk13';
"""

sql = """
DELETE FROM actual_booking_invoices_collection;
"""

sql = """
SELECT salary
FROM actual_booking_invoices_collection;
"""

result = execute_safe_query(sql)

result = execute_safe_query(sql)

print(result)