from app.llm.answer_generator import generate_answer
from app.llm.sql_generator import generate_sql
from app.security.sql_validator import validate_question
from app.services.query_service import execute_safe_query
from app.services.capability_service import SUPPORTED_CAPABILITIES

def ask_finance_question(question: str):

    question_validation = validate_question(question)

    if not question_validation.is_valid:
        raise ValueError(
            question_validation.error
        )

    generated = generate_sql(question)

    query_type = generated.query_type

    is_supported = SUPPORTED_CAPABILITIES.get(
     query_type,
        False
    )

    if not is_supported:
        return {
            "question": question,
            "sql": None,
            "query_type": query_type,
            "data": [],
            "answer": (
                "This question is not supported by the currently available data."
            )
        }

    result = execute_safe_query(
        generated.sql
    )

    answer = generate_answer(
        question=question,
        sql=generated.sql,
        result=result
    )

    return {
        "question": question,
        "sql": generated.sql,
        "query_type": generated.query_type,
        "data": result,
        "answer": answer
    }

def has_data(result: list[dict]) -> bool:

    if not result:
        return False

    for row in result:
        for value in row.values():
            if value is not None:
                return True

    return False