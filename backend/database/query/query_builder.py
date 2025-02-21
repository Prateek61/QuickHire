from typing import Any, Dict, List, Optional, Union, TypeVar, Protocol, TYPE_CHECKING
from abc import ABC, abstractmethod
from psycopg2.extensions import AsIs
from ..engine import DBSession
from .query import Query, QueryParamList
from .base import QueryBuilderBase

if TYPE_CHECKING:
    from ..model.base_schema import BaseSchema

T = TypeVar('T')

class SchemaProtocol(Protocol):
    """Protocol for schema operations to avoid circular imports."""
    @classmethod
    def _table(cls) -> str: ...
    
    @classmethod
    def _get_col(cls, field_name: str) -> str: ...
    
    @classmethod
    def _get_fk(cls, table: Any) -> Optional[str]: ...
    
    @classmethod
    def _get_pk(cls) -> tuple[Optional[str], Any]: ...
    
    @classmethod
    def col(cls, field_name: str) -> AsIs: ...

def _name() -> str:
    """Generate a unique name for query parameters."""
    _name.counter += 1
    return f'p{_name.counter}'
_name.counter = 0

class Alias(ABC):
    def _get(self) -> str:
        pass

def _format_value(value: Any) -> Any:
    """Format a value for use in a query."""
    if isinstance(value, AsIs):
        return value
    if isinstance(value, Statement):
        return AsIs(value.alias) if value.alias else value._get()
    if isinstance(value, Alias):
        return value._get()
    return value

class TableAlias(Alias):
    def __init__(self, table: SchemaProtocol, alias: str):
        self.table = table
        self.alias = alias

    def _get(self) -> AsIs:
        return AsIs(self.alias)
    
    def col(self, name: str) -> AsIs:
        return AsIs(f'{self.alias}.{self.table._get_col(name)}')

    def _get_col(self, name: str) -> str:
        return self.table._get_col(name)

    def _table(self) -> str:
        return self.table._table()

    def _get_fk(self, target: Any) -> Optional[str]:
        return self.table._get_fk(target)

    def _get_pk(self) -> tuple[Optional[str], Any]:
        return self.table._get_pk()
    
class Field(Alias):
    def __init__(self, table: Union[str, SchemaProtocol, TableAlias], name: str):
        self.table = table
        self.name = name

    def _get(self) -> AsIs:
        if isinstance(self.table, (TableAlias, SchemaProtocol)):
            return self.table.col(self.name)
        return AsIs(f'{self.table}.{self.name}')
    
class QueryBuilder(ABC):
    @abstractmethod
    def get_query(self) -> Query:
        pass

    def get_query_str(self, session: DBSession) -> str:
        return self.get_query().construct_query(session)
    
class Condition(QueryBuilder):
    def __init__(self):
        self._query = Query()

    def get_query(self) -> Query:
        return self._query
    
    def gt(self, a: Any, b: Any) -> 'Condition':
        return self._internal_op('>', a, b)
    
    def gte(self, a: Any, b: Any) -> 'Condition':
        return self._internal_op('>=', a, b)
    
    def lt(self, a: Any, b: Any) -> 'Condition':
        return self._internal_op('<', a, b)
    
    def lte(self, a: Any, b: Any) -> 'Condition':
        return self._internal_op('<=', a, b)
    
    def eq(self, a: Any, b: Any) -> 'Condition':
        return self._internal_op('=', a, b)
    
    def neq(self, a: Any, b: Any) -> 'Condition':
        return self._internal_op('<>', a, b)
    
    def and_(self, cond: Any | None = None) -> 'Condition':
        return self._internal_connectors('AND', cond)
    
    def or_(self, cond: Any | None = None) -> 'Condition':
        return self._internal_connectors('OR', cond)
    
    def not_(self, cond: Any | None = None) -> 'Condition':
        return self._internal_connectors('NOT', cond)
    
    def in_(self, a: Any, b: Any) -> 'Condition':
        return self._internal_op('IN', a, b)
    
    def like(self, a: Any, b: Any) -> 'Condition':
        return self._internal_op('LIKE', a, b)
    
    def ilike(self, a: Any, b: Any) -> 'Condition':
        return self._internal_op('ILIKE', a, b)
    
    def not_in(self, a: Any, b: Any) -> 'Condition':
        return self._internal_op('NOT IN', a, b)

    def is_null(self, a: Any) -> 'Condition':
        return self._internal_single_op('IS NULL', a)
    
    def is_not_null(self, a: Any) -> 'Condition':
        return self._internal_single_op('IS NOT NULL', a)
    
    def between(self, a: Any, b: Any, c: Any) -> 'Condition':
        a_name, b_name, c_name = _name(), _name(), _name()

        a_q = self._build_query_part(a, a_name)
        b_q = self._build_query_part(b, b_name)
        c_q = self._build_query_part(c, c_name)

        self._query._query += f"{a_q} BETWEEN {b_q} AND {c_q}"
        return self
    
    def exists(self, a: Any) -> 'Condition':
        return self._internal_single_op('EXISTS', a)
    
    def not_exists(self, a: Any) -> 'Condition':
        return self._internal_single_op('NOT EXISTS', a)
    
    def any(self, a: Any) -> 'Condition':
        return self._internal_single_op('ANY', a)
    
    def all(self, a: Any) -> 'Condition':
        return self._internal_single_op('ALL', a)
    
    def some(self, a: Any) -> 'Condition':
        return self._internal_single_op('SOME', a)

    def _internal_single_op(self, op: str, a: Any) -> 'Condition':
        q = self._build_query_part(a, _name())
        self._query._query += f"{op} ({q})"
        return self

    def _internal_op(self, op: str, a: Any, b: Any) -> 'Condition':
        a_name, b_name = _name(), _name()

        a_q = self._build_query_part(a, a_name)
        b_q = self._build_query_part(b, b_name)

        self._query._query += f"{a_q} {op} {b_q}"
        return self
    
    def _internal_connectors(self, op: str, cond: Any | None = None) -> 'Condition':
        self._query._query += f" {op} "
        if not cond:
            return self
        
        name = _name()
        q = self._build_query_part(cond, name)
        self._query._query += q
        return self
    
    def _build_query_part(self, value: Any, name: str) -> str:
        if isinstance(value, QueryBuilder):
            self._query.add_sub_queries({name: value.get_query()})
            return Query.SUBQUERY_PATTERN % name
        else:
            self._query.add_params({name: _format_value(value)})
            return f"%({name})s"

def _table_str(table: Union[SchemaProtocol, TableAlias]) -> str:
    if isinstance(table, TableAlias):
        return f"{table.table._table()} AS {table.alias}"
    return table._table()

class Select(QueryBuilder):
    """SQL SELECT query builder."""
    def __init__(self, table: Union[SchemaProtocol, TableAlias], *fields: Union[Field, str, AsIs]):
        self._table = table
        self._query = Query()
        self._latest_joined = table

        if fields:
            cols = QueryParamList('%(col)s', [
                {'col': field if isinstance(field, (AsIs, str)) else field._get()}
                for field in fields
            ])
            self._query._query = f"SELECT {Query.SUBQUERY_PATTERN % "cols"} FROM %(table)s"
            self._query.add_sub_queries({'cols': cols})
        else:
            self._query._query = "SELECT * FROM %(table)s"

        self._query.add_params({'table': AsIs(_table_str(table))})

    def get_query(self) -> Query:
        return self._query

    def where(self, condition: Condition) -> 'Select':
        """Add WHERE clause."""
        self._query._query += f" WHERE {Query.SUBQUERY_PATTERN % 'where'}"
        self._query.add_sub_queries({'where': condition.get_query()})
        return self

    def group_by(self, *fields: Union[Field, str]) -> 'Select':
        """Add GROUP BY clause."""
        cols = QueryParamList('%(col)s', [
            {'col': field if isinstance(field, (AsIs, Field)) else Field(self._table, field)}
            for field in fields
        ])
        self._query._query += f" GROUP BY {Query.SUBQUERY_PATTERN % 'group_by'}"
        self._query.add_sub_queries({'group_by': cols})
        return self

    def having(self, condition: Condition) -> 'Select':
        """Add HAVING clause."""
        self._query._query += f" HAVING {Query.SUBQUERY_PATTERN % 'having'}"
        self._query.add_sub_queries({'having': condition.get_query()})
        return self

    def order_by(self, *specs: Union[str, AsIs, Alias, Dict[Union[str, Alias, AsIs], str]]) -> 'Select':
        """Add ORDER BY clause. For each field, you can specify ASC/DESC using a dict."""
        items = []

        for spec in specs:
            if isinstance(spec, dict):
                for field, direction in spec.items():
                    items.append({'col': AsIs(f"{_format_value(field)} {direction.upper()}")})
            else:
                items.append({'col': _format_value(spec)})
        
        self._query._query += f" ORDER BY {Query.SUBQUERY_PATTERN % 'order_by'}"
        self._query.add_sub_queries({'order_by': QueryParamList('%(col)s', items)})
        return self

    def limit(self, limit: int) -> 'Select':
        """Add LIMIT clause."""
        self._query._query += " LIMIT %(limit)s"
        self._query.add_params({'limit': limit})
        return self

    def offset(self, offset: int) -> 'Select':
        """Add OFFSET clause."""
        self._query._query += " OFFSET %(offset)s"
        self._query.add_params({'offset': offset})
        return self

    def join(self,
             table: Union[SchemaProtocol, TableAlias],
             condition: Optional[Condition] = None,
             join_type: str = 'INNER') -> 'Select':
        """
        Add JOIN clause. If condition is not provided, tries to find a foreign key relationship.
        join_type can be: INNER, LEFT, RIGHT, FULL
        """
        # Auto-detect join condition if not provided
        if condition is None:
            # Try to find foreign key from current table to joined table
            fk_name = self._latest_joined._get_fk(table)
            if fk_name:
                # Current table has FK to joined table
                pk_name, _ = table._get_pk()
                condition = Condition().eq(
                    self._latest_joined.col(fk_name),
                    table.col(pk_name)
                )
            else:
                # Try reverse - joined table might have FK to current table
                fk_name = table._get_fk(self._latest_joined)
                if not fk_name:
                    raise ValueError("No foreign key relationship found between tables")
                pk_name, _ = self._latest_joined._get_pk()
                condition = Condition().eq(
                    table.col(fk_name),
                    self._latest_joined.col(pk_name)
                )

        # Add the JOIN clause
        join_type = join_type.upper()
        if join_type not in ('INNER', 'LEFT', 'RIGHT', 'FULL'):
            raise ValueError(f"Invalid join type: {join_type}")

        join_name = _name()
        self._query._query += f" {join_type} JOIN {AsIs(_table_str(table))} ON {Query.SUBQUERY_PATTERN % join_name}"
        self._query.add_sub_queries({join_name: condition.get_query()})
        
        self._latest_joined = table
        return self

    def union(self, other: 'Select', all: bool = False) -> 'Select':
        """Combine with another SELECT using UNION."""
        union_name = _name()
        self._query._query += f" {'UNION ALL' if all else 'UNION'} {Query.SUBQUERY_PATTERN % union_name}"
        self._query.add_sub_queries({union_name: other.get_query()})
        return self

    def intersect(self, other: 'Select', all: bool = False) -> 'Select':
        """Combine with another SELECT using INTERSECT."""
        intersect_name = _name()
        self._query._query += f" {'INTERSECT ALL' if all else 'INTERSECT'} {Query.SUBQUERY_PATTERN % intersect_name}"
        self._query.add_sub_queries({'intersect': other.get_query()})
        return self

    def except_(self, other: 'Select', all: bool = False) -> 'Select':
        """Combine with another SELECT using EXCEPT."""
        except_name = _name()
        self._query._query += f" {'EXCEPT ALL' if all else 'EXCEPT'} {Query.SUBQUERY_PATTERN % except_name}"
        self._query.add_sub_queries({except_name: other.get_query()})
        return self

class Statement(Alias):
    def __init__(self, op: str, col: Union[AsIs, str, Field], alias: Optional[str] = None):
        self.op = op
        self.col = col
        self.alias = alias

    def _get(self) -> AsIs:
        return AsIs(f"{self.op}({_format_value(self.col)}) {f'AS {self.alias}' if self.alias else ''}")
    
    @classmethod
    def count(cls, col: Union[AsIs, str, Field], alias: Optional[str] = None) -> 'Statement':
        return cls('COUNT', col, alias)
    
    @classmethod
    def sum(cls, col: Union[AsIs, str, Field], alias: Optional[str] = None) -> 'Statement':
        return cls('SUM', col, alias)
    
    @classmethod
    def avg(cls, col: Union[AsIs, str, Field], alias: Optional[str] = None) -> 'Statement':
        return cls('AVG', col, alias)
    
    @classmethod
    def min(cls, col: Union[AsIs, str, Field], alias: Optional[str] = None) -> 'Statement':
        return cls('MIN', col, alias)
    
    @classmethod
    def max(cls, col: Union[AsIs, str, Field], alias: Optional[str] = None) -> 'Statement':
        return cls('MAX', col, alias)
    
    @classmethod
    def distinct(cls, col: Union[AsIs, str, Field], alias: Optional[str] = None) -> 'Statement':
        return cls('DISTINCT', col, alias)
    
    @classmethod
    def custom(cls, op: str, col: Union[AsIs, str, Field], alias: Optional[str] = None) -> 'Statement':
        return cls(op, col, alias)
