from app.llm.answer_generator import generate_answer
from app.llm.sql_generator import generate_sql
from app.security.sql_validator import validate_question
from app.services.query_service import execute_safe_query
from app.services.capability_service import is_capability_supported

def ask_finance_question(question: str):

    question_validation = validate_question(question)

    if not question_validation.is_valid:
        raise ValueError(
            question_validation.error
        )

    generated = generate_sql(question)

    if not is_capability_supported(
        generated.query_type
    ):
        return {
            "question": question,
            "sql": None,
            "query_type": generated.query_type,
            "data": [],
            "answer": (
                "This question is not supported by the currently available data."
            )
        }

    result = execute_safe_query(
        generated.sql
    )

    if not has_data(result):
        return {
            "question": question,
            "sql": generated.sql,
            "query_type": generated.query_type,
            "data": result,
            "answer": "No data was found for the requested period."
        }

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