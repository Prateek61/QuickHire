from abc import ABC, abstractmethod
from ..engine import *

from typing import Dict, Any, Iterable

class QueryBase(ABC):
    @abstractmethod
    def construct_query(self, session: DBSession, reconstruct: bool = False) -> str:
        pass

    @abstractmethod
    def _bind_query(self, session: DBSession) -> str:
        pass

    @abstractmethod
    def set_final_query(self, query: str) -> None:
        pass

    @abstractmethod
    def is_constructed(self) -> bool:
        pass
    
    @property
    def query_str(self) -> str:
        pass

class Query(QueryBase):
    def __init__(self, query: str = "", params: Dict[str, Any] = {}, end: bool = True):
        self._query = query
        self._params = params
        self._sub_queries: Dict[str, QueryBase] = {}
        self._final_query = ""
        self._changed = True
        self._end = end

    def construct_query(self, session: DBSession, reconstruct: bool = False) -> str:
        if self.is_constructed() and not reconstruct:
            return self._final_query
        self._final_query = self._bind_query(session)
        self.changed = False
        return self._final_query

    def _bind_query(self, session: DBSession) -> str:
        binded_query: str = self._query
        if self._sub_queries:
            binded_query = self._bind_sub_queries(binded_query, session)
        if self._params:
            binded_query = session.cursor.mogrify(binded_query, self._params).decode("utf-8")
        if self._end:
            binded_query += ";"
        return binded_query

    def set_final_query(self, query: str) -> None:
        self._final_query = query
        self.changed = False

    def is_constructed(self) -> bool:
        return not self._changed and bool(self._final_query)
    
    @property
    def query_str(self) -> str:
        if self.is_constructed():
            return self._final_query
        return self._query

    def add_sub_queries(self, sub_queries: Dict[str, QueryBase]) -> None:
        self._sub_queries.update(sub_queries)
        self.changed = True
    
    def get_sub_queries(self) -> Dict[str, QueryBase]:
        return self._sub_queries
    
    def remove_sub_queries(self, keys: Iterable[str]) -> None:
        for key in keys:
            self._sub_queries.pop(key, None)

    def get_main_query(self) -> str:
        return self._query

    def set_query(self, query: str) -> None:
        self._query = query
        self.changed = True

    def add_params(self, params: Dict[str, Any]) -> None:
        self._params.update(params)
        self.changed = True

    def remove_params(self, keys: Iterable[str]) -> None:
        for key in keys:
            self._params.pop(key, None)

    def get_params(self) -> Dict[str, Any]:
        return self._params

    def _bind_sub_queries(self, query: str, session: DBSession) -> str:
        for key, sub_query in self._sub_queries.items():
            sub_query_str: str = ""
            if sub_query.is_constructed():
                sub_query_str = sub_query.query_str
            else:
                sub_query_str = sub_query.construct_query(session)

            query = query.replace(f"%%({key})%%", sub_query_str)
        return query

class QueryParamList(QueryBase):
    def __init__(self, query: str = "", params: Iterable[Dict[str, Any]] = []):
        self._query = query
        self._params = params
        self._final_query = ""
        self._changed = False

    def construct_query(self, session: DBSession, reconstruct: bool = False) -> str:
        if self.is_constructed() and not reconstruct:
            return self._final_query
        self._final_query = self._bind_query(session)
        self._changed = False
        return self._final_query

    def _bind_query(self, session: DBSession) -> str:
        binded_query: str = ",".join(session.cursor.mogrify(self._query, i).decode("utf-8")
                                    for i in self._params)
        return binded_query

    def set_final_query(self, query: str) -> None:
        self._final_query = query
        self.changed = False

    def is_constructed(self) -> bool:
        return not self._changed and bool(self._final_query)

    def add_params(self, params: Iterable[Dict[str, Any]]) -> None:
        self._params.extend(params)
        self.changed = True

    def remove_params(self, indices: Iterable[int]) -> None:
        for index in indices:
            self._params.pop(index)
        self.changed = True

    def get_params(self) -> Iterable[Dict[str, Any]]:
        return self._params

    @property
    def query_str(self) -> str:
        return self._final_query
