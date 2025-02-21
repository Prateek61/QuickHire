from ..connection import PostgresConnection
from psycopg2.extensions import cursor

from typing import Any

class Session:
    def __init__(self, connection: PostgresConnection, log: bool = False):
        self.connection = connection
        self.cursor: cursor = connection.cursor()
        self.log = log
        self._active = True

    def __enter__(self) -> 'Session':
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def close(self) -> None:
        if not self._active:
            return
        self._active = False
        self.cursor.close()

    def commit(self) -> None:
        self.connection.connection.commit()

    def __destroy__(self) -> None:
        self.close()

    def rollback(self) -> None:
        self.connection.connection.rollback()

    def execute(self, query_str: str, force_log=False):
        if force_log or self.log:
            print(f"Execuring query: {query_str}")
        self.cursor.execute(query_str)
    