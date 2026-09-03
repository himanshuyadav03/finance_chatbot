from dataclasses import dataclass

import sqlglot
from sqlglot import exp



@dataclass
class QuestionValidationResult:
    is_valid: bool
    error: str | None = None


BLOCKED_INTENTS = {
    "delete",
    "remove",
    "drop",
    "truncate",
    "update",
    "insert",
    "create",
    "alter",
    "grant",
    "revoke",
}


@dataclass
class ValidationResult:
    is_valid: bool
    error: str | None = None


ALLOWED_TABLES = {
    "actual_booking_invoices_collection",
    "booking_to_invoice_forecasting",
    "invoice_to_cash_forecasting",
}


ALLOWED_COLUMNS = {
    "actual_booking_invoices_collection": {
        "id",
        "booking_week",
        "booking_amount",
        "invoice_week",
        "invoice_amount",
        "collection_week",
        "collection_amount",
    },

    "booking_to_invoice_forecasting": {
        "id",
        "booking_week",
        "lag_0",
        "lag_1",
        "lag_2",
        "lag_3",
        "lag_4",
        "lag_5",
        "lag_6",
        "lag_7",
        "lag_8",
        "lag_9",
        "lag_10",
        "booking_amount",
        "forecasted_invoice",
    },

    "invoice_to_cash_forecasting": {
        "id",
        "invoice_week",
        "lag_0",
        "lag_1",
        "lag_2",
        "lag_3",
        "lag_4",
        "lag_5",
        "lag_6",
        "lag_7",
        "lag_8",
        "lag_9",
        "lag_10",
        "invoice_amount",
        "forecasted_collection",
    },
}

BLOCKED_OPERATIONS = (
    exp.Insert,
    exp.Update,
    exp.Delete,
    exp.Drop,
    exp.Create,
    exp.Alter,
)


def validate_question(question: str) -> QuestionValidationResult:

    if not question or not question.strip():
        return QuestionValidationResult(
            is_valid=False,
            error="Question cannot be empty."
        )

    question_lower = question.lower()

    for word in BLOCKED_INTENTS:

        if word in question_lower:
            return QuestionValidationResult(
                is_valid=False,
                error=(
                    "This chatbot supports read-only finance questions. "
                    "Data modification requests are not allowed."
                )
            )

    return QuestionValidationResult(is_valid=True)


def validate_sql(sql: str) -> ValidationResult:

    if not sql or not sql.strip():
        return ValidationResult(
            is_valid=False,
            error="SQL query is empty."
        )

    try:
        statements = sqlglot.parse(
            sql,
            read="postgres"
        )
    except sqlglot.errors.ParseError:
        return ValidationResult(
            is_valid=False,
            error="Invalid SQL syntax."
        )

    # Only one SQL statement is allowed
    if len(statements) != 1:
        return ValidationResult(
            is_valid=False,
            error="Multiple SQL statements are not allowed."
        )

    statement = statements[0]

    # Block dangerous operations
    for operation in BLOCKED_OPERATIONS:
        if statement.find(operation):
            return ValidationResult(
                is_valid=False,
                error=f"{operation.__name__} operation is not allowed."
            )

    # Only SELECT queries are allowed
    if not isinstance(statement, exp.Select):
        return ValidationResult(
            is_valid=False,
            error="Only SELECT queries are allowed."
        )

    # Extract tables
    tables = {
        table.name
        for table in statement.find_all(exp.Table)
    }

    # Extract columns
    columns = {
        column.name
        for column in statement.find_all(exp.Column)
    }

    # Validate tables
    unknown_tables = tables - ALLOWED_TABLES

    if unknown_tables:
        return ValidationResult(
            is_valid=False,
            error=f"Unknown table(s): {', '.join(sorted(unknown_tables))}"
        )

    # Validate columns
    if len(tables) == 1:
        table_name = next(iter(tables))

        allowed_columns = ALLOWED_COLUMNS[table_name]

        unknown_columns = columns - allowed_columns

        if unknown_columns:
            return ValidationResult(
                is_valid=False,
                error=(
                    "Unknown column(s): "
                    + ", ".join(sorted(unknown_columns))
                )
            )

    return ValidationResult(is_valid=True)