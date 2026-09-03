from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.chat import AskRequest, AskResponse
from app.services.chat_service import ask_finance_question

router = APIRouter()

@router.post(
    "/ask",
    response_model=AskResponse
)

def ask_question(request: AskRequest):

    try:
        result = ask_finance_question(
            request.question
        )

        return {
            "question": result["question"],
            "answer": result["answer"],
            "query_type": result["query_type"],
            "data": result["data"],
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database query failed."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unable to process the question."
        )