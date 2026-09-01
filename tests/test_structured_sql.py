from app.llm.sql_generator import generate_sql


question = "What was total booking in 2025Q1?"
question = "What is total forecasted collection for 2025Q3?"

result = generate_sql(question)


print("SQL:")
print(result.sql)

print("\nTable:")
print(result.table)

print("\nQuery Type:")
print(result.query_type)

print("\nExplanation:")
print(result.explanation)