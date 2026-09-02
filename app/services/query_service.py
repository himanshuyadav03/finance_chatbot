from app.database.executor import execute_query
from app.security.sql_validator import validate_sql


def execute_safe_query(sql: str):

    validation = validate_sql(sql)

    if not validation.is_valid:
        raise ValueError(
            f"SQL validation failed: {validation.error}"
        )

    result = execute_query(sql)

    return result