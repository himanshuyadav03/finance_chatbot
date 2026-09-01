from dataclasses import dataclass

import sqlglot
from sqlglot import exp


@dataclass
class ValidationResult:
    is_valid: bool
    error: str | None = None


ALLOWED_TABLES = {
    "actual_booking_invoices_collection",
    "booking_to_invoice_forecasting",
    "invoice_to_cash_forecasting",
}


BLOCKED_OPERATIONS = (
    exp.Insert,
    exp.Update,
    exp.Delete,
    exp.Drop,
    exp.Create,
    exp.Alter,
)


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

    # Only SELECT-style queries
    if not isinstance(statement, exp.Select):
        return ValidationResult(
            is_valid=False,
            error="Only SELECT queries are allowed."
        )

    # Check tables
    tables = {
        table.name
        for table in statement.find_all(exp.Table)
    }

    unknown_tables = tables - ALLOWED_TABLES

    if unknown_tables:
        return ValidationResult(
            is_valid=False,
            error=f"Unknown table(s): {', '.join(unknown_tables)}"
        )

    return ValidationResult(is_valid=True)