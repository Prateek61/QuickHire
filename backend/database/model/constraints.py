from typing import Optional

class TableConstraint:
    """Base class for table-level constraints."""
    
    def get_constraint_sql(self) -> str:
        """Get the SQL for this constraint."""
        raise NotImplementedError()

class UniqueConstraint(TableConstraint):
    """Unique constraint across multiple columns."""
    
    def __init__(self, *columns: str, name: Optional[str] = None):
        """Initialize unique constraint.
        
        Args:
            *columns: Columns to include in constraint
            name: Optional constraint name
        """
        self.columns = columns
        self.name = name or f"unique_{'_'.join(columns)}"
    
    def get_constraint_sql(self) -> str:
        return f"CONSTRAINT {self.name} UNIQUE ({', '.join(self.columns)})"

class CheckConstraint(TableConstraint):
    """Table-level CHECK constraint."""
    
    def __init__(self, condition: str, name: Optional[str] = None):
        """Initialize check constraint.
        
        Args:
            condition: SQL condition for CHECK
            name: Optional constraint name
        """
        self.condition = condition
        self.name = name or f"check_{hash(condition)}"
    
    def get_constraint_sql(self) -> str:
        return f"CONSTRAINT {self.name} CHECK ({self.condition})"

class Index:
    """Class representing a database index."""
    
    def __init__(self, 
                 *columns: str,
                 name: Optional[str] = None,
                 unique: bool = False,
                 method: str = 'btree',
                 where: Optional[str] = None):
        """Initialize an index.
        
        Args:
            *columns: Columns to include in the index
            name: Optional custom index name
            unique: Whether this is a unique index
            method: Index method (btree, hash, gist, etc.)
            where: Optional partial index condition
        """
        self.columns = columns
        self.name = name or f"idx_{'_'.join(columns)}"
        self.unique = unique
        self.method = method
        self.where = where
    
    def get_creation_sql(self, table_name: str) -> str:
        """Generate SQL for creating this index.
        
        Args:
            table_name: Name of the table
            
        Returns:
            str: CREATE INDEX statement
        """
        parts = []
        parts.append("CREATE")
        
        if self.unique:
            parts.append("UNIQUE")
            
        parts.append("INDEX")
        parts.append(self.name)
        parts.append(f"ON {table_name}")
        
        if self.method != 'btree':
            parts.append(f"USING {self.method}")
            
        parts.append(f"({', '.join(self.columns)})")
        
        if self.where:
            parts.append(f"WHERE {self.where}")
            
        return " ".join(parts)