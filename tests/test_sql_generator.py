from app.llm.sql_generator import generate_sql


# question = "What was total booking in 2025?"
question = "What is forecasted invoice for 2025Wk05?"
question = "What percentage of booking is invoiced within 3 weeks?"

sql = generate_sql(question)

print("Question:")
print(question)

print("\nGenerated SQL:")
print(sql)