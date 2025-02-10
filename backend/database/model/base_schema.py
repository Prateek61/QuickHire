from abc import ABC, abstractmethod
from marshmallow import Schema, fields
from psycopg2.extensions import cursor as Cursor, AsIs

from typing import Dict, Any, Iterable, Tuple, TYPE_CHECKING

from .fields import DatabaseFieldBase, PrimaryKey

from ..query.query import Query, QueryParamList
from ..query.queries import QUERIES

class BaseSchema(Schema, ABC):
    @classmethod
    def _table(cls) -> str:
        """Returns the table name of the schema.
        """
        # Check if the class has a variable named table_name
        if hasattr(cls, "table_name"):
            return getattr(cls, "table_name").lower()
        return cls.__name__.lower().removesuffix("schema").lower()
    
    @classmethod
    def _fields(cls) -> Dict[str, DatabaseFieldBase]:
        return cls._declared_fields
    
    @classmethod
    def col(cls, field_name: str) -> str:
        return AsIs(f'{cls._table()}.{cls._get_col(field_name)}')

    @classmethod
    def _get_col_from_field(cls, field: DatabaseFieldBase) -> str:
        if field.db_column:
            return field.db_column
        # Find the field in the declared fields
        for name, f in cls._fields().items():
            if f == field:
                return name

    @classmethod
    def _get_col(cls, field_name: str) -> str:
        fields = cls._fields()
        if fields[field_name].db_column:
            return fields[field_name].db_column
        return field_name
    
    @classmethod
    def _get_column_name_with_field(cls, field_name: str, field: DatabaseFieldBase) -> str:
        if field.db_column:
            return field.db_column
        return field_name

    @classmethod
    def _get_column_names(cls) -> Iterable[str]:
        return [cls._get_column_name_with_field(field_name, field) for field_name, field in cls._fields().items()]
    
    @classmethod
    def _get_column_names_str(cls) -> str:
        return ", ".join(cls._get_column_names())
    
    @classmethod
    def _get_pk(cls) -> Tuple[str, PrimaryKey]:
        for field_name, field in cls._fields().items():
            if isinstance(field, PrimaryKey):
                return field_name, field
        return None, None
    
    @classmethod
    def _get_table_creation_query(cls, extra: str = "") -> Query:
        base_query = Query(QUERIES['create_table'], {
            'table_name': AsIs(cls._table()),
            'extra': AsIs(extra)
        })
        columns = QueryParamList("%(column_name)s %(creation_query)s", [])
        
        params = [
            {
                'column_name': AsIs(cls._get_column_name_with_field(field_name, field)),
                'creation_query': AsIs(field.get_column_creation_query())
            } for field_name, field in cls._fields().items()
        ]
        columns.add_params(params)

        base_query.add_sub_queries({
            'columns': columns
        })
        return base_query
    
    @classmethod
    def _get_fk(cls, table: 'BaseSchema') -> str:
        from .fields import ForeignKey

        for field_name, field in cls._fields().items():
            if isinstance(field, ForeignKey) and field._ref_schema == table:
                return field_name
        return None
