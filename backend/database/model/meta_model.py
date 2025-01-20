from abc import ABC, abstractmethod

class MetaModel(ABC):
    def __init__(self, child: type, **kwargs):
        self.table_name = kwargs.get("name", child.__name__.lower())
