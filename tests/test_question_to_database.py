from app.llm.sql_generator import generate_sql
from app.services.query_service import execute_safe_query


question = "What was total booking in 2025Q1?"

print("Question:")
print(question)


generated = generate_sql(question)

print("\nGenerated SQL:")
print(generated.sql)


result = execute_safe_query(
    generated.sql
)

print("\nDatabase Result:")
print(result)