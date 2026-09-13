def build_chart_config(
    data: list[dict],
    query_type: str
) -> dict | None:

    if not data:
        return None

    mapping = {
        "actual_booking": {
            "chart_type": "line",
            "x": "booking_week",
            "y": "booking_amount"
        },

        "actual_invoice": {
            "chart_type": "line",
            "x": "invoice_week",
            "y": "invoice_amount"
        },

        "actual_collection": {
            "chart_type": "line",
            "x": "collection_week",
            "y": "collection_amount"
        }
    }

    return mapping.get(query_type)