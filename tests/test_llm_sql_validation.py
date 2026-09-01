from app.llm.sql_generator import generate_sql
from app.security.sql_validator import validate_sql


question = "What was total booking in 2025Q1?"

result = generate_sql(question)

print("Question:")
print(question)

print("\nGenerated SQL:")
print(result.sql)

validation = validate_sql(result.sql)

print("\nValidation:")
print(validation)