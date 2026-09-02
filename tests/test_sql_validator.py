from app.security.sql_validator import validate_sql


sql = """
SELECT SUM(booking_amount)
FROM actual_booking_invoices_collection
WHERE booking_week BETWEEN '2025Wk01' AND '2025Wk13';
"""

sql = """
DELETE FROM actual_booking_invoices_collection;
"""

sql = """
UPDATE actual_booking_invoices_collection
SET booking_amount = 0;
"""

sql = """
SELECT SUM(revenue)
FROM company_revenue;
"""


sql = """
SELECT *
FROM actual_booking_invoices_collection;

DROP TABLE actual_booking_invoices_collection;
"""

sql = """
SELECT
    SUM(booking_amount)
FROM actual_booking_invoices_collection
WHERE booking_week = '2025Wk05';
"""

sql = """
SELECT
    SUM(revenue)
FROM actual_booking_invoices_collection;
"""
sql = """
SELECT SUM(forecasted_invoice)
FROM booking_to_invoice_forecasting
WHERE booking_week BETWEEN '2025Wk01' AND '2025Wk13';
"""

sql = """
SELECT SUM(forecasted_collection)
FROM booking_to_invoice_forecasting;
"""

result = validate_sql(sql)

print(result)