from app.llm.client import client


def generate_answer(
    question: str,
    sql: str,
    result
) -> str:

    prompt = f"""
You are a finance chatbot.

Answer the user's question using ONLY the database result provided below.

IMPORTANT RULES:

1. Never invent financial values.
2. Never change the numeric result.
3. Do not perform additional calculations unless clearly required.
4. If the database result is empty, say that no data was found.
5. Keep the answer concise and finance-friendly.
6. Do not mention SQL unless the user asks about it.
7. Use readable number formatting.

Examples:
2487654321.32 -> 2.49 billion
325400000.00 -> 325.4 million

USER QUESTION:
{question}

SQL USED:
{sql}

DATABASE RESULT:
{result}

Return only the final answer for the user.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text.strip()