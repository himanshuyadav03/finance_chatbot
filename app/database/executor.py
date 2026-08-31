from sqlalchemy import text

from app.database.connection import engine

def execute_query(query: str):
    with engine.connect() as connection:
        result = connection.execute(text(query))

        rows = result.fetchall()
        columns = result.keys()


        return [
            dict(zip(columns, row))
            for row in rows
        ]