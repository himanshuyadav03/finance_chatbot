from typing import Any, Literal

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


class ChartConfig(BaseModel):

    chart_type: str
    x: str
    y:str

class AskResponse(BaseModel):
    question: str
    answer: str
    query_type: str

    response_type : Literal["text", "table", "chart"]

    data: list[dict[str, Any]]

    chart: ChartConfig | None = None
