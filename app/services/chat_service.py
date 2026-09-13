from app.llm.answer_generator import generate_answer
from app.llm.sql_generator import generate_sql

from app.security.sql_validator import validate_question

from app.services.query_service import execute_safe_query
from app.services.capability_service import is_capability_supported
from app.services.conversation_service import (
    add_message,
    get_conversation,
)


def ask_finance_question(
    question: str,
    session_id: str
):

    # 1. Validate user question
    question_validation = validate_question(question)

    if not question_validation.is_valid:
        raise ValueError(
            question_validation.error
        )

    # 2. Get previous conversation history
    history = get_conversation(
        session_id
    )

    # 3. Generate SQL using question + history
    generated = generate_sql(
        question=question,
        conversation_history=history
    )

    # 4. Check whether current data supports this query type
    if not is_capability_supported(
        generated.query_type
    ):

        answer = (
            "This question is not supported by "
            "the currently available data."
        )

        add_message(
            session_id=session_id,
            role="user",
            content=question
        )

        add_message(
            session_id=session_id,
            role="assistant",
            content=answer
        )

        return {
            "question": question,
            "sql": None,
            "query_type": generated.query_type,
            "data": [],
            "answer": answer
        }

    # 5. Execute validated SQL
    result = execute_safe_query(
        generated.sql
    )

    # 6. Handle no-data result
    if not has_data(result):

        answer = (
            "No data was found for the requested period."
        )

        add_message(
            session_id=session_id,
            role="user",
            content=question
        )

        add_message(
            session_id=session_id,
            role="assistant",
            content=answer
        )

        return {
            "question": question,
            "sql": generated.sql,
            "query_type": generated.query_type,
            "data": result,
            "answer": answer
        }

    # 7. Generate readable answer
    answer = generate_answer(
        question=question,
        sql=generated.sql,
        result=result
    )

    # 8. Store conversation
    add_message(
        session_id=session_id,
        role="user",
        content=question
    )

    add_message(
        session_id=session_id,
        role="assistant",
        content=answer
    )

    # 9. Return API response
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