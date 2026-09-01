from app.llm.sql_generator import generate_sql


# questions = [
#     "What was total booking in 2025Q1?",
#     "What was total invoice in 2025Q2?",
#     "What was total collection in 2025Q3?"
# ]
questions = [
    "How much booking did we have in Q2 2025?",
    "Show me total invoice for the fourth quarter of 2025.",
    "How much cash did we collect in 2025Wk20?",
    "Give me forecasted invoice for Q3 2025.",
    "What percent of bookings convert to invoice within 3 weeks?"
]


for question in questions:

    sql = generate_sql(question)

    print("\nQuestion:")
    print(question)

    print("\nGenerated SQL:")
    print(sql)

    print("-" * 60)