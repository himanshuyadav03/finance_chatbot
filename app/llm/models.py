from typing import Literal

from pydantic import BaseModel


class SQLGenerationResult(BaseModel):
    sql: str
    table: str
    query_type: str
    explanation: str
    response_type: Literal[
        "text",
        "table",
        "chart"
    ]