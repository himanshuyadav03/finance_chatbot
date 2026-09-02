from app.llm.sql_generator import generate_sql
from app.security.sql_validator import validate_sql


questions = [
    "What was total booking in 2025Q1?",
    "What was total invoice in 2025Q2?",
    "What was collection in 2025Wk05?",
    "What is total forecasted invoice for 2025Q3?",
    "What is forecasted collection for 2025Wk10?",
]


for question in questions:

    result = generate_sql(question)

    validation = validate_sql(result.sql)

    print("\nQuestion:")
    print(question)

    print("\nSQL:")
    print(result.sql)

    print("\nValidation:")
    print(validation)

    print("-" * 60)

