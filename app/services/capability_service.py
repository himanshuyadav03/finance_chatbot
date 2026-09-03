from app.metadata.loader import load_all_metadata


CAPABILITY_REQUIREMENTS = {
    "actual_booking": {
        "table": "actual_booking_invoices_collection",
        "columns": ["booking_week", "booking_amount"],
    },

    "actual_invoice": {
        "table": "actual_booking_invoices_collection",
        "columns": ["invoice_week", "invoice_amount"],
    },

    "actual_collection": {
        "table": "actual_booking_invoices_collection",
        "columns": ["collection_week", "collection_amount"],
    },

    "booking_to_invoice_linearity": {
        "table": "booking_to_invoice_forecasting",
        "columns": ["booking_week", "lag_0"],
    },

    "invoice_to_cash_linearity": {
        "table": "invoice_to_cash_forecasting",
        "columns": ["invoice_week", "lag_0"],
    },

    "forecasted_invoice": {
        "table": "booking_to_invoice_forecasting",
        "columns": ["forecasted_invoice"],
    },

    "forecasted_collection": {
        "table": "invoice_to_cash_forecasting",
        "columns": ["forecasted_collection"],
    },
}

def is_capability_supported(query_type: str) -> bool:

    requirement = CAPABILITY_REQUIREMENTS.get(query_type)

    if requirement is None:
        return False

    metadata = load_all_metadata()

    columns_metadata = metadata["columns"]

    table_name = requirement["table"]
    required_columns = requirement["columns"]

    table_columns = columns_metadata.get(
        table_name,
        {}
    )

    return all(
        column in table_columns
        for column in required_columns
    )