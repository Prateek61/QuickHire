from abc import ABC, abstractmethod
from typing import Dict, Any, Iterable, Tuple, List, Optional, TypeVar, Type, Set, Union, Generic, TYPE_CHECKING
from marshmallow import Schema, fields, ValidationError, post_load
from psycopg2.extensions import cursor as Cursor, AsIs
from dataclasses import dataclass, field
from datetime import datetime
import re

from .fields import DatabaseFieldBase, PrimaryKey
from .constraints import TableConstraint, Index
from ..engine import DBSession
from ..query import Query, QueryParamList, QUERIES
from ..query.base import QueryBuilderBase

# Forward references for type checking
if TYPE_CHECKING:
    from ..query.query_builder import Select, Condition

# Type variables
T = TypeVar('T', bound='BaseDataClass')

class BaseDataClass(ABC):
    """Base class for database table data classes.
    """
    pass

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

class BaseSchema(Schema, ABC, Generic[T], metaclass=ModelSchemaMeta):
    """Base class for database table schemas."""

    # Class-level configuration
    __abstract__ = True  # Whether this is an abstract base class
    __table_args__ = None  # Additional table arguments (constraints, indexes, etc.)
    __initializing__ = False  # Flag to prevent validation during initialization
    __data_class__ = BaseDataClass  # Data class associated with this schema

    # Core database operations
    @classmethod
    def get_by_id(cls, session: DBSession, id_value: Any) -> Optional[T]:
        """Get a record by its primary key."""
        from ..query.query_builder import Select, Condition
        
        pk_name, _ = cls._get_pk()
        if not pk_name:
            raise ValueError(f"Schema {cls.__name__} has no primary key")
        
        condition = Condition().eq(cls.col(pk_name), id_value)
        query = Select(cls).where(condition).get_query()
        return QueryHelper.fetch_one(query, session, cls)

    @classmethod
    def get_all(cls, session: DBSession,
                order_by: Optional[List[str]] = None,
                limit: Optional[int] = None,
                offset: Optional[int] = None) -> List[T]:
        """Get all records with optional ordering and pagination."""
        from ..query.query_builder import Select
        
        query = Select(cls)
        
        if order_by:
            query.order_by(*[cls.col(field) for field in order_by])
        if limit is not None:
            query.limit(limit)
        if offset is not None:
            query.offset(offset)
            
        return QueryHelper.fetch_multiple(query.get_query(), session, cls)

    @classmethod
    def filter_by(cls, session: DBSession,
                  filters: Dict[str, Any],
                  order_by: Optional[List[str]] = None) -> List[T]:
        """Get records matching the given filters."""
        from ..query.query_builder import Select, Condition
        
        condition = Condition()
        first = True
        
        for field, value in filters.items():
            if first:
                condition.eq(cls.col(field), value)
                first = False
            else:
                condition.and_().eq(cls.col(field), value)
                
        query = Select(cls).where(condition)
        
        if order_by:
            query.order_by(*[cls.col(field) for field in order_by])
            
        return QueryHelper.fetch_multiple(query.get_query(), session, cls)

    @classmethod
    def exists_by_field(cls, session: DBSession, field: str, value: Any) -> bool:
        """Check if a record exists with the given field value."""
        from ..query.query_builder import Select, Condition
        
        condition = Condition().eq(cls.col(field), value)
        query = Select(cls).where(condition).limit(1)
        return bool(QueryHelper.fetch_one_raw(query.get_query(), session))
    
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
    def serialize_single(cls, data: Dict[str, Any]) -> T:
        """Serialize single object to data class."""
        return cls.__data_class__(**data)
    
    @classmethod
    def load_multiple(cls, data: List[Dict[str, Any]]) -> List[T]:
        """Deserialize multiple objects to data class."""
        return [cls.serialize_single(item) for item in data]
    
    @post_load
    def make_data(self, data: Dict[str, Any], **kwargs) -> T:
        """Deserialize data to data class."""
        return self.serialize_single(data)

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
        session.execute(creation_query.construct_query(session))
        
        # Create triggers
        for trigger_query in cls._get_trigger_creation_queries():
            trigger_query.set_end()
            session.execute(trigger_query.construct_query(session))
        
        # Create indexes
        for index_sql in cls._get_indexes():
            session.execute(index_sql)

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
    
    @classmethod
    def _get_insert_query(cls, 
                        fields: Optional[List[str]] = None) -> Tuple[Query, QueryParamList]:
        """Generate INSERT query for this record."""
        if fields is None:
            fields = [
                name for name, field in cls._fields().items()
                if not field.is_auto()
            ]

        returning_fields = [
            name for name, field in cls._fields().items()
            if field.is_auto()
        ]
        
        columns = [cls._get_col(field) for field in fields]
        values = [f"%({field})s" for field in fields]
        return_columns = [cls._get_col(field) for field in returning_fields]
        
        sql = f"""
        INSERT INTO {cls._table()}
            ({', '.join(columns)})
        VALUES
            {Query.SUBQUERY_PATTERN % 'values'}
        """
        
        if return_columns:
            sql += f" RETURNING {', '.join(return_columns)}"
        
        qp = QueryParamList("(" + ", ".join(values) + ")")

        q = Query(sql, {})
        return q, qp
    
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

class QueryHelper:
    @staticmethod
    def run(query: Query, session: DBSession, force_log: bool = True) -> None:
        """Execute a query without returning results."""
        query_str = query.construct_query(session=session)
        session.cursor.execute(query_str)

        if force_log:
            print(f"Executed Query: {query_str}")

    @staticmethod
    def fetch_one_raw(query: Query, session: DBSession) -> Optional[Dict[str, Any]]:
        """Fetch a single row as a dictionary."""
        query_str = query.construct_query(session=session)
        session.cursor.execute(query_str)
        result = session.cursor.fetchone()
        if result:
            return {key: result[key] for key in result.keys()}
        return None
    
    @staticmethod
    def fetch_multiple_raw(query: Query, session: DBSession) -> List[Dict[str, Any]]:
        """Fetch multiple rows as dictionaries."""
        query_str = query.construct_query(session=session)
        session.cursor.execute(query_str)
        results = session.cursor.fetchall()
        return [{key: row[key] for key in row.keys()} for row in results]
    
    @staticmethod
    def fetch_one(query: Query, session: DBSession, schema: Type[BaseSchema[T]]) -> Optional[T]:
        """Fetch and deserialize a single row."""
        raw = QueryHelper.fetch_one_raw(query, session)
        if raw:
            return schema().load(raw)
        return None
    
    @staticmethod
    def fetch_multiple(query: Query, session: DBSession, schema: Type[BaseSchema[T]]) -> List[T]:
        """Fetch and deserialize multiple rows."""
        raw = QueryHelper.fetch_multiple_raw(query, session)
        return schema(many=True).load(raw)
    
    @staticmethod
    def insert(data: Union[T, List[T]], schema: Type[BaseSchema[T]], session: DBSession) -> Union[T, List[T]]:
        """Insert one or more records."""
        single_item = not isinstance(data, list)
        items = [data] if single_item else data
            
        insert_query, query_param = schema._get_insert_query()
        dumped = schema(many=True).dump(items)
        query_param.add_params(dumped)
        insert_query.add_sub_queries({'values': query_param})
        QueryHelper.run(insert_query, session)

        # Update data with auto-generated fields
        returning_fields = [
            (name, field) for name, field in schema._fields().items()
            if field.is_auto()
        ]

        if returning_fields:
            returning_data = session.cursor.fetchall()
            for i, item in enumerate(items):
                for name, field in returning_fields:
                    col_name = schema._get_col_from_field(field)
                    row_dict = {key: returning_data[i][key] for key in returning_data[i].keys()}
                    setattr(item, name, row_dict[col_name])

        return items[0] if single_item else items
    