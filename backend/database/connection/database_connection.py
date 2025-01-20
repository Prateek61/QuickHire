from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, Union

import psycopg2
from psycopg2.extensions import cursor as psycopg2_cursor

class DatabaseConnection(ABC):
    def __init__(self, config: Dict[str, str] | None = None, url: str | None = None, autocommit: bool = True):
        if config:
            self.initialize_connection(config, autocommit=autocommit)
        elif url:
            self.initialize_connection_url(url, autocommit=autocommit)
        else:
            raise ValueError("Either config or url must be provided")

    @abstractmethod
    def initialize_connection(self, config: Dict[str, str], autocommit: bool) -> None:
        pass
    
    @abstractmethod
    def initialize_connection_url(self, url: str, autocommit: bool) -> None:
        pass

    @abstractmethod
    def cursor(self) -> psycopg2_cursor:
        pass

    @abstractmethod
    def close_connection(self) -> None:
        pass

    def _debug_execute(self, query: str) -> psycopg2_cursor:
        cursor = self.cursor()
        cursor.execute(query)
        return cursor
    