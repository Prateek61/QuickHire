from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime

from marshmallow import fields, ValidationError

class DBType(Enum):
    INTEGER = "INTEGER"
    TEXT = "TEXT"
    VARCHAR = "VARCHAR"
    SERIAL = "SERIAL"
    DATE = "DATE"
    TIMESTAMP = "TIMESTAMP"

# Custom database fields, which are inherited from marshmallow fields, just with some additional parameters
class DatabaseFieldBase(fields.Field, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._db_column = kwargs.pop("column", None)
        self._db_required = kwargs.get("required", False)
        self._db_unique = kwargs.pop("unique", False)
        self._db_allow_null = self.allow_none
        self._default = kwargs.get("default", None)

    @property
    def db_column(self) -> str:
        return self._db_column
    
    @property
    def db_required(self) -> bool:
        return self._db_required
    
    @property
    def db_unique(self) -> bool:
        return self._db_unique

    @property
    def db_type(self) -> DBType:
        raise ValueError("Cant get db_type from DatabaseFieldBase")

    def get_column_creation_query(self) -> str:
        return f"{self.db_type.value} {self.column_creation_postfix()}"

    def column_creation_postfix(self) -> str:
        postfix = ""
        if self.db_unique:
            postfix += " UNIQUE"
        if self.db_required:
            postfix += " NOT NULL"
        return postfix

class PrimaryKey(DatabaseFieldBase, fields.Integer):
    def __init__(self, **kwargs):
        # Initialie both parent classes
        DatabaseFieldBase.__init__(self, **kwargs)
        fields.Integer.__init__(self, **kwargs)

    @property
    def db_type(self) -> DBType:
        return DBType.SERIAL
    
    def get_column_creation_query(self) -> str:
        return f"{self.db_type.value} PRIMARY KEY"
    
class Integer(DatabaseFieldBase, fields.Integer):
    def __init__(self, **kwargs):
        DatabaseFieldBase.__init__(self, **kwargs)
        fields.Integer.__init__(self, **kwargs)

    @property
    def db_type(self) -> DBType:
        return DBType.INTEGER

class Text(DatabaseFieldBase, fields.String):
    def __init__(self, **kwargs):
        DatabaseFieldBase.__init__(self, **kwargs)
        fields.String.__init__(self, **kwargs)

    @property
    def db_type(self) -> DBType:
        return DBType.TEXT

class Varchar(DatabaseFieldBase, fields.String):
    def __init__(self, len: int, **kwargs):
        self._len = len
        DatabaseFieldBase.__init__(self, **kwargs)
        fields.String.__init__(self, **kwargs)

    @property
    def db_type(self) -> DBType:
        return DBType.VARCHAR 
    
    def get_column_creation_query(self) -> str:
        return f"{self.db_type.value}({self._len}) {self.column_creation_postfix()}"

from .base_schema import BaseSchema

class ForeignKey(DatabaseFieldBase, fields.Integer):
    def __init__(self, ref_schema: BaseSchema, on_delete: str = "", **kwargs):
        # Assert that the ref_schema is a subclass of BaseSchema
        if not issubclass(ref_schema, BaseSchema):
            raise ValueError("ref_schema must be a subclass of BaseSchema")
        
        self._on_delete = on_delete
        self._ref_schema: BaseSchema = ref_schema
        self._ref_table_name: str = self._ref_schema._table()
        
        self.pk_name, self.pk_field = self._ref_schema._get_pk()

        DatabaseFieldBase.__init__(self, **kwargs)
        fields.Integer.__init__(self, **kwargs)

    @property
    def db_type(self) -> DBType:
        return DBType.INTEGER
    
    def get_column_creation_query(self) -> str:
        res = f"{self.db_type.value} {self.column_creation_postfix()} REFERENCES {self._ref_table_name}({self.pk_name})"
        if self._on_delete == 'cascade':
            res += " ON DELETE CASCADE"
        elif self._on_delete == 'set_null':
            res += " ON DELETE SET NULL"
        elif self._on_delete == 'set_default':
            res += " ON DELETE SET DEFAULT"

        return res


class Date(DatabaseFieldBase, fields.Date):
    def __init__(self, **kwargs):
        DatabaseFieldBase.__init__(self, **kwargs)
        fields.Date.__init__(self, **kwargs)

    @property
    def db_type(self) -> DBType:
        return DBType.DATE
    
class Timestamp(DatabaseFieldBase, fields.DateTime):
    def __init__(self, **kwargs):
        DatabaseFieldBase.__init__(self, **kwargs)
        fields.DateTime.__init__(self, **kwargs)

    @property
    def db_type(self) -> DBType:
        return DBType.TIMESTAMP
