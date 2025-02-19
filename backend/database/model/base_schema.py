from abc import ABC, abstractmethod
from typing import Dict, Any, Iterable, Tuple, List, Optional, TypeVar, Type, Set, Union
from marshmallow import Schema, fields, ValidationError
from psycopg2.extensions import cursor as Cursor, AsIs
import re

from .fields import DatabaseFieldBase, PrimaryKey
from .constraints import TableConstraint, Index
from ..engine import DBSession
from ..query import Query, QueryParamList, QUERIES

# Type variables
T = TypeVar('T')

class ModelSchemaMeta(type(Schema)):
    """Metaclass for BaseSchema that handles automatic initialization of schema classes."""
    
    def __new__(mcs, name, bases, attrs):
        # Create the class
        cls = super().__new__(mcs, name, bases, attrs)
        
        # Skip initialization for BaseSchema itself
        if name == 'BaseSchema':
            return cls
            
        # Check if this class explicitly declares itself as abstract
        # Don't inherit __abstract__ from parent classes
        is_abstract = '__abstract__' in attrs and attrs['__abstract__']
        
        if is_abstract:
            return cls
            
        # Initialize declared fields
        if hasattr(cls, '_declared_fields'):
            for field_name, field in cls._declared_fields.items():
                if hasattr(field, '_post_init'):
                    field._post_init(cls, field_name)
            
        # Bind foreign keys
        cls._bind_foreign_keys()

        # Validate schema
        cls._validate_schema()
            
        return cls

class BaseSchema(Schema, ABC, metaclass=ModelSchemaMeta):
    """Base class for database table schemas."""

    # Class-level configuration
    __abstract__ = True  # Whether this is an abstract base class
    __table_args__ = None  # Additional table arguments (constraints, indexes, etc.)
    __initializing__ = False  # Flag to prevent validation during initialization
    
    @classmethod
    def _validate_schema(cls):
        """Validate schema configuration."""
        # Ensure table name is valid
        table_name = cls._table()
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table_name):
            raise ValueError(f"Invalid table name: {table_name}")
        
        # Ensure primary key exists
        pk_name, pk_field = cls._get_pk()
        if not pk_name and not cls.__abstract__:
            raise ValueError(f"Schema {cls.__name__} must have a primary key")
        
        # Validate foreign key references
        cls._validate_foreign_keys()
    
    @classmethod
    def _validate_foreign_keys(cls):
        """Validate foreign key configurations."""
        from .fields import ForeignKey
        
        for field_name, field in cls._fields().items():
            if isinstance(field, ForeignKey):
                if not field.pk_name and field._ref_schema != 'self':
                    raise ValueError(
                        f"Foreign key {field_name} references schema "
                        f"{field._ref_schema.__name__ if field._ref_schema else 'Unknown'} "
                        "which has no primary key"
                    )
    
    @classmethod
    def _table(cls) -> str:
        """Get the table name for this schema."""
        if hasattr(cls, "table_name"):
            return getattr(cls, "table_name").lower()
        return cls.__name__.lower().removesuffix("schema")
    
    @classmethod
    def _fields(cls) -> Dict[str, DatabaseFieldBase]:
        """Get all database fields."""
        return cls._declared_fields
    
    @classmethod
    def col(cls, field_name: str) -> AsIs:
        """Get fully qualified column name."""
        return AsIs(f'{cls._table()}.{cls._get_col(field_name)}')

    @classmethod
    def _get_col_from_field(cls, field: DatabaseFieldBase) -> str:
        """Get column name for a field instance."""
        if field.db_column:
            return field.db_column
            
        for name, f in cls._fields().items():
            if f == field:
                return name
        raise ValueError(f"Field {field} not found in schema {cls.__name__}")

    @classmethod
    def _get_col(cls, field_name: str) -> str:
        """Get column name for a field by name."""
        fields = cls._fields()
        if field_name not in fields:
            raise ValueError(f"Field {field_name} not found in schema {cls.__name__}")
            
        if fields[field_name].db_column:
            return fields[field_name].db_column
        return field_name
    
    @classmethod
    def col(cls, field_name: str) -> str:
        """Get fully qualified column name."""
        return AsIs(f'{cls._table()}.{cls._get_col(field_name)}')

    @classmethod
    def _get_column_names(cls) -> List[str]:
        """Get all column names."""
        return [cls._get_col(name) for name in cls._fields()]
    
    @classmethod
    def _get_column_names_str(cls) -> str:
        """Get comma-separated list of column names."""
        return ", ".join(cls._get_column_names())
    
    @classmethod
    def _get_pk(cls) -> Tuple[Optional[str], Optional[PrimaryKey]]:
        """Get primary key field."""
        for field_name, field in cls._fields().items():
            if isinstance(field, PrimaryKey):
                return field_name, field
        return None, None
    
    @classmethod
    def _get_indexes(cls) -> List[str]:
        """Get index creation SQL statements."""
        indexes = []
        table = cls._table()
        
        # Add indexes for indexed fields
        for field_name, field in cls._fields().items():
            column = cls._get_col(field_name)
            if field.db_index:
                sql = field.get_index_creation_query(table, column)
                if sql:
                    indexes.append(sql)
        
        # Add composite indexes from table args
        if cls.__table_args__:
            for arg in cls.__table_args__:
                if isinstance(arg, Index):
                    indexes.append(arg.get_creation_sql(table))
        
        return indexes
    
    @classmethod
    def _get_table_constraints(cls) -> List[str]:
        """Get table constraint SQL."""
        constraints = []
        
        if cls.__table_args__:
            for arg in cls.__table_args__:
                if isinstance(arg, TableConstraint):
                    constraints.append(arg.get_constraint_sql())
        
        return constraints
    
    @classmethod
    def _get_extra_sql(cls) -> Optional[str]:
        """Get extra SQL for table creation."""
        constraints = cls._get_table_constraints()
        if constraints:
            return ", " + ", ".join(constraints)
        return None

    @classmethod
    def _get_table_creation_query(cls) -> Query:
        """Generate table creation SQL."""
        # Initialize table creation query
        query = Query(QUERIES['create_table'], {
            'table_name': AsIs(cls._table())
        })
        
        # Add column definitions
        columns = QueryParamList("%(column_name)s %(creation_query)s", [])
        params = []
        
        for field_name, field in cls._fields().items():
            params.append({
                'column_name': AsIs(cls._get_col(field_name)),
                'creation_query': AsIs(field.get_column_creation_query())
            })
        
        columns.add_params(params)
        query.add_sub_queries({'columns': columns})
        
        # Add table constraints as extra SQL
        extra_sql = cls._get_extra_sql()
        query.add_sub_queries({'extra': Query(extra_sql if extra_sql else "")})
        
        return query
    
    @classmethod
    def _get_trigger_creation_queries(cls) -> List[Query]:
        """Get queries for creating triggers."""
        queries = []
        table_name = cls._table()
        
        for field_name, field in cls._fields().items():
            if hasattr(field, 'get_trigger_sql'):
                trigger_sql = field.get_trigger_sql(table_name, cls._get_col(field_name))
                if trigger_sql:
                    queries.append(Query(trigger_sql))
        
        return queries

    @classmethod
    def create_table(cls, session: DBSession):
        """Create table and related objects (triggers, indexes, etc.)."""
        # Create table
        creation_query = cls._get_table_creation_query()
        session.execute(creation_query)
        
        # Create triggers
        for trigger_query in cls._get_trigger_creation_queries():
            session.execute(trigger_query)
        
        # Create indexes
        for index_sql in cls._get_indexes():
            session.execute(Query(index_sql))

    @classmethod
    def _bind_foreign_keys(cls):
        """Bind foreign key constraints."""
        from .fields import ForeignKey
        
        for field_name, field in cls._fields().items():
            if isinstance(field, ForeignKey):
                field._bind_to_schema(cls)

    @classmethod
    def _get_fk(cls, table: Type[T]) -> Optional[str]:
        """Get foreign key field referencing another table."""
        from .fields import ForeignKey
        
        for field_name, field in cls._fields().items():
            if isinstance(field, ForeignKey) and field._ref_schema == table:
                return field_name
        return None
    
    def get_update_query(self, 
                        fields: Optional[List[str]] = None,
                        where: Optional[str] = None) -> Query:
        """Generate UPDATE query for this record."""
        cls = self.__class__
        pk_name, _ = cls._get_pk()
        
        if fields is None:
            fields = [
                name for name, field in self._fields().items()
                if not isinstance(field, PrimaryKey)
            ]
        
        # Build SET clause
        set_items = []
        params = {}
        
        for field in fields:
            column = cls._get_col(field)
            set_items.append(f"{column} = %({field})s")
            params[field] = getattr(self, field)
        
        set_clause = ', '.join(set_items)
        
        # Build WHERE clause
        if where is None:
            where = f"{pk_name} = %({pk_name})s"
            params[pk_name] = getattr(self, pk_name)
        
        sql = f"""
        UPDATE {cls._table()}
        SET {set_clause}
        WHERE {where}
        """
        
        return Query(sql, params)
    
    def get_insert_query(self, 
                        fields: Optional[List[str]] = None) -> Query:
        """Generate INSERT query for this record."""
        cls = self.__class__
        
        if fields is None:
            fields = [
                name for name, field in self._fields().items()
                if not isinstance(field, PrimaryKey) or getattr(self, name) is not None
            ]
        
        columns = [cls._get_col(field) for field in fields]
        values = [f"%({field})s" for field in fields]
        
        params = {
            field: getattr(self, field)
            for field in fields
        }
        
        sql = f"""
        INSERT INTO {cls._table()} 
            ({', '.join(columns)})
        VALUES
            ({', '.join(values)})
        """
        
        return Query(sql, params)
    
    @classmethod
    def get_delete_query(cls,
                        where: str,
                        params: Optional[Dict[str, Any]] = None) -> Query:
        """Generate DELETE query."""
        sql = f"""
        DELETE FROM {cls._table()}
        WHERE {where}
        """
        
        return Query(sql, params or {})
