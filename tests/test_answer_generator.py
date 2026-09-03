from app.llm.answer_generator import generate_answer


question = "What was total booking in 2025Q1?"

sql = """
SELECT SUM(booking_amount) AS total_booking
FROM actual_booking_invoices_collection
WHERE booking_week BETWEEN '2025Wk01' AND '2025Wk13';
"""

result = [
    {
        "total_booking": 2487654321.32
    }
]

answer = generate_answer(
    question=question,
    sql=sql,
    result=result
)

print(answer)