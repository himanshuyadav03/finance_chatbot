from app.services.chat_service import ask_finance_question


question = "What was total booking in 2025Q1?"

question = "What is total forecasted collection for 2025Q3?"

response = ask_finance_question(question)

print("Question:")
print(response["question"])

print("\nSQL:")
print(response["sql"])

print("\nDatabase Result:")
print(response["data"])

print("\nAnswer:")
print(response["answer"])