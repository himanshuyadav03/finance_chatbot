from app.llm.client import client
from app.metadata.loader import load_all_metadata


def generate_sql(question: str):

    metadata = load_all_metadata()

    prompt = f"""
You are an expert PostgreSQL SQL generator for a finance chatbot.

Your job is to convert a finance user's question into PostgreSQL SQL.

DATABASE METADATA:
{metadata}

IMPORTANT RULES:

1. Generate only SELECT queries.

2. Never generate:
INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE
CREATE

3. Use only tables and columns available in the metadata.

4. For actual booking, invoice, or collection questions,
use the actual_booking_invoices_collection table.

5. For forecasted invoice questions,
use booking_to_invoice_forecasting.

6. For forecasted collection questions,
use invoice_to_cash_forecasting.

7. forecasted_invoice is already the final forecast after
booking-to-invoice waterfall logic.

Do not recalculate forecasted_invoice using booking_amount and lag columns.

8. forecasted_collection is already the final forecast after
invoice-to-cash waterfall logic.

Do not recalculate forecasted_collection using invoice_amount and lag columns.

9. Lag values are decimals.

Example:
0.15 means 15%.

10. Only use lag columns when the user specifically asks
about linearity, lag, conversion timing, or percentage conversion.

USER QUESTION:
{question}

Return only the PostgreSQL SQL query.
Do not include markdown.
Do not explain the query.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text.strip()