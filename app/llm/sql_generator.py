from app.llm.client import client
from app.metadata.loader import load_all_metadata
from app.llm.prompts import build_sql_prompt


def generate_sql(question: str):

    metadata = load_all_metadata()

    prompt = build_sql_prompt(
        question=question,
        metadata=metadata
    )

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    sql = response.output_text.strip()

    return sql