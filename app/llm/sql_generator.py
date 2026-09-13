from app.llm.client import client
from app.llm.models import SQLGenerationResult
from app.llm.prompts import build_sql_prompt
from app.rag.retriever import retrieve_metadata


def generate_sql(
    question: str,
    conversation_history: list | None = None
) -> SQLGenerationResult:

    retrieved_context = retrieve_metadata(
        question=question,
        top_k=5
    )

    prompt = build_sql_prompt(
        question=question,
        retrieved_context=retrieved_context,
        conversation_history=conversation_history
    )

    response = client.responses.parse(
        model="gpt-5-mini",
        input=prompt,
        text_format=SQLGenerationResult
    )

    return response.output_parsed