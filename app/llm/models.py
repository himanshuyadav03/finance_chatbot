from pydantic import BaseModel


class SQLGenerationResult(BaseModel):
    sql: str
    table: str
    query_type: str
    explanation: str