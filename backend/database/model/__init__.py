"""Database model system providing field types, constraints, and schema management."""

from .fields import (
    # Base field
    DatabaseFieldBase,
    
    # Primary and foreign keys
    PrimaryKey,
    ForeignKey,
    
    # Numeric fields
    Integer,
    Numeric,
    
    # String fields
    Text,
    Varchar,
    
    # Date and time fields
    Date,
    Time,
    Timestamp,
    
    # Other scalar fields
    Boolean,
    
    # Complex fields
    JSON,
    Array
)

from .constraints import (
    # Table constraints
    TableConstraint,
    UniqueConstraint,
    CheckConstraint,
    
    # Indexing
    Index
)

from .base_schema import BaseSchema

__all__ = [
    # Fields
    'DatabaseFieldBase',
    'PrimaryKey',
    'ForeignKey',
    'Integer',
    'Numeric',
    'Text',
    'Varchar',
    'Date',
    'Time',
    'Timestamp',
    'Boolean',
    'JSON',
    'Array',
    
    # Constraints
    'TableConstraint',
    'UniqueConstraint',
    'CheckConstraint',
    'Index',
    
    # Base Schema
    'BaseSchema'
]