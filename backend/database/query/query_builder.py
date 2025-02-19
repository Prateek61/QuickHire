from ..model.base_schema import BaseSchema
from .query import QueryBase, Query, QueryParamList
from psycopg2.extensions import AsIs
from typing import List
from abc import ABC, abstractmethod
from ..engine import DBSession

from typing import Any, Dict

def _get_random_name() -> str:
    import random
    import string
    return "".join(random.choices(string.ascii_letters, k=10))

class QueryBuilder(ABC):
    @abstractmethod
    def get_query(self) -> Query:
        pass

    def get_query_str(self, session: DBSession) -> str:
        return self.get_query().construct_query(session)

def _format_param(value: Any) -> Any:
    """Helper function to format parameters consistently"""
    if isinstance(value, str) and any(op in value for op in ['COUNT', 'SUM', 'AVG', 'MIN', 'MAX']):
        return AsIs(value)
    return value
    
class ConditionQueryBuilder(QueryBuilder):
    def __init__(self):
        self._query = Query(end=False)

    def get_query(self) -> Query:
        return self._query
    
    def greater_than(self, a: Any, b: Any) -> 'ConditionQueryBuilder':
        return self._internal_make_query(a, b, '>')
    
    def less_than(self, a: Any, b: Any) -> 'ConditionQueryBuilder':
        return self._internal_make_query(a, b, '<')
    
    def greater_than_equal(self, a: Any, b: Any) -> 'ConditionQueryBuilder':
        return self._internal_make_query(a, b, '>=')
    
    def less_than_equal(self, a: Any, b: Any) -> 'ConditionQueryBuilder':
        return self._internal_make_query(a, b, '<=')
    
    def equal(self, a: Any, b: Any) -> 'ConditionQueryBuilder':
        return self._internal_make_query(a, b, '=')
    
    def not_equal(self, a: Any, b: Any) -> 'ConditionQueryBuilder':
        return self._internal_make_query(a, b, '!=')
    
    def like(self, a: Any, b: Any) -> 'ConditionQueryBuilder':
        return self._internal_make_query(a, b, 'LIKE')
    
    def ilike(self, a: Any, b: Any) -> 'ConditionQueryBuilder':
        return self._internal_make_query(a, b, 'ILIKE')
    
    def in_(self, a: Any, b: Any) -> 'ConditionQueryBuilder':
        return self._internal_make_query(a, b, 'IN')
    
    def not_in(self, a: Any, b: Any) -> 'ConditionQueryBuilder':
        return self._internal_make_query(a, b, 'NOT IN')
    
    def and_(self, cond: Any | None = None) -> 'ConditionQueryBuilder':
        return self._internal_connectors('AND', cond)
    
    def or_(self, cond: Any | None = None) -> 'ConditionQueryBuilder':
        return self._internal_connectors('OR', cond)
    
    def not_(self, cond: Any | None = None) -> 'ConditionQueryBuilder':
        return self._internal_connectors('NOT', cond)

    def _internal_make_query(self, a: Any, b: Any, op: str) -> 'ConditionQueryBuilder':
        a_name = _get_random_name()
        b_name = _get_random_name()

        if isinstance(a, QueryBuilder):
            a_query_str = f'%%({a_name})%%'
            self._query.add_sub_queries({a_name: a.get_query()})
        else:
            a_query_str = f'%({a_name})s'
            self._query.add_params({a_name: _format_param(a)})

        if isinstance(b, QueryBuilder):
            b_query_str = f'%%({b_name})%%'
            self._query.add_sub_queries({b_name: b.get_query()})
        else:
            b_query_str = f'%({b_name})s'
            self._query.add_params({b_name: _format_param(b)})

        self._query._query += f"{a_query_str} {op} {b_query_str}"
        return self
    
    def _internal_connectors(self, connector: str, cond: Any | None = None) -> 'ConditionQueryBuilder':
        self._query._query += f' {connector} '
        
        if not cond:
            return self
        
        name = _get_random_name()
        if isinstance(cond, QueryBuilder):
            self._query.add_sub_queries({name: cond.get_query()})
            self._query._query += f'%%({name})%%'
        else:
            self._query.add_params({name: _format_param(cond)})
            self._query._query += f'%({name})s'

        return self
    
class SelectQueryBuilder(QueryBuilder):
    def __init__(self, table: BaseSchema, *columns):
        self._table = table
        self._latest_joined = table
        if columns:
            column_selection_query = QueryParamList('%(column_name)s', [
                {'column_name': col} for col in columns
            ])
        else:
            column_selection_query = Query('*', end=False)

        self._query = Query('SELECT %%(column_selection)%% FROM %(table_name)s', end=False)
        self._query.add_params({'table_name': AsIs(table._table())})
        self._query.add_sub_queries({'column_selection': column_selection_query})

    def get_query(self) -> Query:
        return self._query
    
    def where(self, cond: ConditionQueryBuilder) -> 'SelectQueryBuilder':
        self._query._query += ' WHERE %%(where)%%'
        self._query.add_sub_queries({'where': cond.get_query()})
        return self
    
    def having(self, cond: ConditionQueryBuilder) -> 'SelectQueryBuilder':
        self._query._query += ' HAVING %%(having)%%'
        self._query.add_sub_queries({'having': cond.get_query()})
        return self
    
    def group_by(self, *columns: str) -> 'SelectQueryBuilder':
        column_selection_query = QueryParamList('%(column_name)s', [
            {'column_name': AsIs(col)} for col in columns
        ])
        self._query._query += ' GROUP BY %%(group_by)%%'
        self._query.add_sub_queries({'group_by': column_selection_query})
        return self
    
    def join(self, table: BaseSchema, cond: ConditionQueryBuilder | None = None, join_type: str = 'INNER') -> 'SelectQueryBuilder':
        if cond:
            return self._internal_join(table, cond, join_type)
        
        # Find the foreign key
        fk_name = self._latest_joined._get_fk(table)
        if fk_name:
            pk_name, _ = table._get_pk()
            pk = table.col(pk_name)
            fk = self._latest_joined.col(fk_name)
        else:
            fk_name = table._get_fk(self._latest_joined)
            if not fk_name:
                raise ValueError("No foreign key found")
            pk_name, _ = self._latest_joined._get_pk()
            pk = self._latest_joined.col(pk_name)
            fk = table.col(fk_name)
        
        self._latest_joined = table
        return self._internal_join(table, ConditionQueryBuilder().equal(fk, pk), join_type)

    def _internal_join(self, table: BaseSchema, cond: ConditionQueryBuilder, join_type: str) -> 'SelectQueryBuilder':
        self._query._query += f' {join_type} JOIN {AsIs(table._table())} ON %%(join_condition)%%'
        self._query.add_sub_queries({'join_condition': cond.get_query()})
        return self
    