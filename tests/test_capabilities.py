from app.services.capability_service import is_capability_supported


query_types = [
    "actual_booking",
    "actual_invoice",
    "actual_collection",
    "booking_to_invoice_linearity",
    "invoice_to_cash_linearity",
    "forecasted_invoice",
    "forecasted_collection",
]


for query_type in query_types:

    supported = is_capability_supported(
        query_type
    )

    print(
        f"{query_type}: {supported}"
    )