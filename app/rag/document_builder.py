from app.metadata.loader import load_all_metadata


def build_metadata_documents() -> list[str]:
    metadata = load_all_metadata()

    documents = []

    tables = metadata.get("tables", {})
    columns = metadata.get("columns", {})
    business_rules = metadata.get("business_rules", {})
    relationships = metadata.get("relationships", {})
    fiscal_calendar = metadata.get("fiscal_calendar", {})
    sql_examples = metadata.get("sql_examples", {})

    # Tables
    for table_name, table_info in tables.items():
        documents.append(
            f"""
Table: {table_name}

Description:
{table_info}
""".strip()
        )

    # Columns
    for table_name, table_columns in columns.items():

        for column_name, column_info in table_columns.items():

            documents.append(
                f"""
Table: {table_name}
Column: {column_name}

Details:
{column_info}
""".strip()
            )

    # Business Rules
    for rule_name, rule_info in business_rules.items():

        documents.append(
            f"""
Business Rule: {rule_name}

Details:
{rule_info}
""".strip()
        )

    # Relationships
    for relationship_name, relationship_info in relationships.items():

        documents.append(
            f"""
Relationship: {relationship_name}

Details:
{relationship_info}
""".strip()
        )

    # Fiscal Calendar
    documents.append(
        f"""
Fiscal Calendar:

{fiscal_calendar}
""".strip()
    )

    # SQL Examples
    examples = sql_examples.get(
        "examples",
        []
    )

    for example in examples:

        documents.append(
            f"""
SQL Example

Question:
{example.get("question")}

SQL:
{example.get("sql")}
""".strip()
        )

    return documents