from app.llm.client import client
from app.llm.models import SQLGenerationResult
from app.llm.prompts import build_sql_prompt
from app.metadata.loader import load_all_metadata


def generate_sql(question: str) -> SQLGenerationResult:

    metadata = load_all_metadata()

    prompt = build_sql_prompt(
        question=question,
        metadata=metadata
    )

    response = client.responses.parse(
        model="gpt-5-mini",
        input=prompt,
        text_format=SQLGenerationResult
    )

    return response.output_parsed