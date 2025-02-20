from .database_connection import DatabaseConnection
import psycopg2
from psycopg2.extensions import cursor as psycopg2_cursor
import psycopg2.extras

from dataclasses import dataclass, field
from marshmallow import Schema, fields, post_load, ValidationError

from typing import Dict

@dataclass
class PostgresConfig:
    database: str
    user: str
    password: str
    host: str
    port: str

    def __str__(self):
        return f"PostgresConfig(database={self.database}, user={self.user}, password={self.password}, host={self.host}, port={self.port})"
    
class PostgresConfigSchema(Schema):
    database = fields.Str(required=True)
    user = fields.Str(required=True)
    password = fields.Str(required=True)
    host = fields.Str(required=True)
    port = fields.Str(required=True)
    
    @post_load
    def make_postgres_config(self, data, **kwargs):
        return PostgresConfig(**data)
    
class PostgresDatabaseConnection(DatabaseConnection):
    def initialize_connection(self, config: Dict[str, str], autocommit: bool):
        schema = PostgresConfigSchema()

        try:
            self.config: PostgresConfig = schema.load(config)
        except ValidationError as e:
            raise ValueError(f"PostgresConfiguration: {e}")
        
        self.connection = psycopg2.connect(
            database=self.config.database,
            user=self.config.user,
            password=self.config.password,
            host=self.config.host,
            port=self.config.port,
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        self.connection.autocommit = autocommit

    def initialize_connection_url(self, url: str, autocommit: bool):
        self.connection = psycopg2.connect(url, cursor_factory=psycopg2.extras.RealDictCursor)
        self.connection.autocommit = autocommit

    def cursor(self) -> psycopg2_cursor:
        return self.connection.cursor()
    
    def close_connection(self):
        self.connection.close()

    def __enter__(self) -> 'PostgresDatabaseConnection':
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()

    def __destroy__(self):
        self.close_connection()

    def __str__(self):
        return f"PostgresDatabaseConnection(config={self.config})"