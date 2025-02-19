from abc import ABC, abstractmethod
from typing import Dict, Any, Iterable, Optional, Union
from ..engine import DBSession
import re

class QueryError(Exception):
    """Custom exception for query-related errors that occur during query construction or parameter binding."""
    pass

class QueryBase(ABC):
    """Abstract base class defining the interface for all query types."""
    
    @abstractmethod
    def construct_query(self, session: DBSession, reconstruct: bool = False) -> str:
        """Construct and return the final SQL query string."""
        pass

    @abstractmethod
    def _bind_query(self, session: DBSession) -> str:
        """Bind parameters to the query template."""
        pass

    @abstractmethod
    def is_constructed(self) -> bool:
        """Check if the query is constructed and up to date."""
        pass
    
    @property
    @abstractmethod
    def query_str(self) -> str:
        """Get the current query string."""
        pass

class Query(QueryBase):
    """Class representing a single SQL query with optional subqueries."""
    
    SUBQUERY_PATTERN = "{{%s}}"  # Format for subquery placeholders
    
    def __init__(self, query: str = "", params: Optional[Dict[str, Any]] = None, end: bool = False):
        """Initialize a new Query instance."""
        self._query = self._normalize_query(query)
        self._params = params or {}
        self._sub_queries: Dict[str, QueryBase] = {}
        self._final_query = ""
        self._is_dirty = True
        self._end = end

    def _normalize_query(self, query: str) -> str:
        """Clean and normalize the query string."""
        # Remove comments and normalize whitespace
        lines = []
        for line in query.splitlines():
            # Remove inline comments
            line = re.sub(r'/\*.*?\*/', '', line)
            line = re.sub(r'--.*$', '', line)
            # Clean whitespace
            line = line.strip()
            if line:
                lines.append(line)
        return ' '.join(lines)

    def _format_sql(self, query: str) -> str:
        """Format SQL query for proper syntax and readability."""
        
        # Clean up unnecessary whitespace while preserving SQL structure
        query = re.sub(r'\s+', ' ', query)
        query = query.strip()
        
        # Add semicolon if needed and requested
        if self._end and not query.rstrip().endswith(';'):
            query += ";"
            
        return query

    def construct_query(self, session: DBSession, reconstruct: bool = False) -> str:
        """Construct the complete SQL query with parameters and subqueries."""
        if self.is_constructed() and not reconstruct:
            return self._final_query
            
        try:
            bound_query = self._bind_query(session)
            self._final_query = self._format_sql(bound_query)
            self._is_dirty = False
            return self._final_query
        except Exception as e:
            raise QueryError(f"Failed to construct query: {str(e)}") from e

    def _bind_query(self, session: DBSession) -> str:
        """Bind all parameters and subqueries to the query."""
        query = self._query
        
        if self._sub_queries:
            query = self._bind_sub_queries(query, session)
            
        if self._params:
            try:
                query = session.cursor.mogrify(query, self._params).decode("utf-8")
            except Exception as e:
                raise QueryError(f"Parameter binding failed: {str(e)}") from e
                
        return query

    def _bind_sub_queries(self, query: str, session: DBSession) -> str:
        """Replace subquery placeholders with their constructed queries."""
        for key, sub_query in self._sub_queries.items():
            placeholder = self.SUBQUERY_PATTERN % key
            if placeholder not in query:
                raise QueryError(f"Subquery placeholder {placeholder} not found in query")
                
            sub_query_str = (sub_query.query_str if sub_query.is_constructed() 
                           else sub_query.construct_query(session))
            query = query.replace(placeholder, sub_query_str)
        return query

    def is_constructed(self) -> bool:
        """Check if the query is constructed and up to date."""
        return not self._is_dirty and bool(self._final_query)

    @property
    def query_str(self) -> str:
        """Get the current query string."""
        return self._final_query if self.is_constructed() else self._query

    def add_sub_queries(self, sub_queries: Dict[str, QueryBase]) -> 'Query':
        """Add multiple subqueries to the query."""
        self._sub_queries.update(sub_queries)
        self._is_dirty = True
        return self

    def add_sub_query(self, key: str, query: QueryBase) -> 'Query':
        """Add a single subquery to the query."""
        self._sub_queries[key] = query
        self._is_dirty = True
        return self

    def remove_sub_queries(self, keys: Iterable[str]) -> 'Query':
        """Remove specified subqueries from the query."""
        for key in keys:
            self._sub_queries.pop(key, None)
        self._is_dirty = True
        return self

    def set_query(self, query: str) -> 'Query':
        """Set a new query template."""
        self._query = self._normalize_query(query)
        self._is_dirty = True
        return self

    def add_params(self, params: Dict[str, Any]) -> 'Query':
        """Add multiple parameters to the query."""
        self._params.update(params)
        self._is_dirty = True
        return self

    def set_param(self, key: str, value: Any) -> 'Query':
        """Set a single parameter value."""
        self._params[key] = value
        self._is_dirty = True
        return self

    def remove_params(self, keys: Iterable[str]) -> 'Query':
        """Remove specified parameters from the query."""
        for key in keys:
            self._params.pop(key, None)
        self._is_dirty = True
        return self

    def clear_params(self) -> 'Query':
        """Remove all parameters from the query."""
        self._params.clear()
        self._is_dirty = True
        return self

    @property
    def params(self) -> Dict[str, Any]:
        """Get a copy of the current parameters."""
        return self._params.copy()

    @property
    def main_query(self) -> str:
        """Get the original query template."""
        return self._query
    
    def set_end(self) -> 'Query':
        """Set the query to end with a semicolon."""
        self._end = True
        return self
    
    def set_no_end(self) -> 'Query':
        """Set the query to not end with a semicolon."""
        self._end = False
        return self

class QueryParamList(Query):
    """Class for handling queries with lists of parameters, typically for bulk operations."""
    
    def __init__(self, query: str = "", params: Optional[Iterable[Dict[str, Any]]] = None):
        """Initialize a new QueryParamList instance."""
        super().__init__(query, end=False)
        self._param_list = list(params or [])

    def _bind_query(self, session: DBSession) -> str:
        """Bind parameters and join the results with commas."""
        try:
            bound_queries = []
            for params in self._param_list:
                bound_query = session.cursor.mogrify(self._query, params).decode("utf-8")
                bound_query = bound_query.strip().rstrip(',')
                bound_queries.append(bound_query)
            return ", ".join(bound_queries)
        except Exception as e:
            raise QueryError(f"Failed to bind parameter list: {str(e)}") from e

    def add_params(self, params: Iterable[Dict[str, Any]]) -> 'QueryParamList':
        """Add multiple sets of parameters."""
        self._param_list.extend(params)
        self._is_dirty = True
        return self

    def add_param_set(self, params: Dict[str, Any]) -> 'QueryParamList':
        """Add a single set of parameters."""
        self._param_list.append(params)
        self._is_dirty = True
        return self

    def remove_params(self, indices: Iterable[int]) -> 'QueryParamList':
        """Remove parameter sets at specified indices."""
        for index in sorted(indices, reverse=True):
            if 0 <= index < len(self._param_list):
                self._param_list.pop(index)
        self._is_dirty = True
        return self

    @property
    def params(self) -> list[Dict[str, Any]]:
        """Get a copy of all parameter sets."""
        return self._param_list.copy()
