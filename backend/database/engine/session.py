from database.connection import PostgresConnection
from psycopg2.extensions import cursor

from typing import Any

class Session:
    def __init__(self, connection: PostgresConnection):
        self.connection = connection
        self.cursor: cursor = connection.cursor()

    def __enter__(self) -> 'Session':
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def close(self) -> None:
        self.cursor.close()

    def commit(self) -> None:
        self.connection.connection.commit()

    def __destroy__(self) -> None:
        self.close()

    def rollback(self) -> None:
        self.connection.connection.rollback()

    def execute(self, query: str) -> cursor:
        self.cursor.execute(query)
        return cursor
    