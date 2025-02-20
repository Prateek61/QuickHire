"""Base interfaces for query components to prevent circular imports."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, TypeVar

T = TypeVar('T')

class QueryBuilderBase(ABC):
    """Base interface for query builders."""
    @abstractmethod
    def get_query(self) -> 'QueryBase':
        pass

class QueryBase(ABC):
    """Base interface for queries."""
    @abstractmethod
    def construct_query(self, session: Any, reconstruct: bool = False) -> str:
        pass
    
    @abstractmethod
    def _bind_query(self, session: Any) -> str:
        pass
    
    @abstractmethod
    def is_constructed(self) -> bool:
        pass
    
    @property
    @abstractmethod
    def query_str(self) -> str:
        pass