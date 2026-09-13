from typing import Any

from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    question: str = Field(
        min_length=1,
        description="Finance question in natural language"
    )

    session_id: str = Field(
        min_length=1,
        description="Conversation session identifier"
    )

class AskResponse(BaseModel):
    question: str
    answer: str
    query_type: str
    data: list[dict[str, Any]]
