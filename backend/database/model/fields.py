from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, date, time
from decimal import Decimal
from typing import Any, Optional, Union, List, Dict, Type

from marshmallow import fields, ValidationError
import marshmallow
from psycopg2.extensions import AsIs

class DBType(Enum):
    """Database column types"""
    INTEGER = "INTEGER"
    BIGINT = "BIGINT"
    SMALLINT = "SMALLINT"
    TEXT = "TEXT"
    VARCHAR = "VARCHAR"
    SERIAL = "SERIAL"
    BIGSERIAL = "BIGSERIAL"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"
    TIME = "TIME"
    TIMESTAMP = "TIMESTAMP"
    DECIMAL = "DECIMAL"
    NUMERIC = "NUMERIC"
    JSON = "JSON"
    JSONB = "JSONB"
    ARRAY = "ARRAY"

class ConstraintViolation(Exception):
    """Raised when a field constraint is violated."""
    pass

class DatabaseFieldBase(fields.Field, ABC):
    """Base class for all database fields."""
    
    def __init__(self, 
                 column: Optional[str] = None,
                 required: bool = False,
                 unique: bool = False,
                 index: bool = False,
                 default: Any = None,
                 check: Optional[str] = None,
                 **kwargs):
        """Initialize a database field."""
        super().__init__(**kwargs)
        self._db_column = column
        self._db_required = required
        self._db_unique = unique
        self._db_index = index
        self._db_check = check
        self._default = default
        self._db_allow_null = self.allow_none

    @property
    def db_column(self) -> Optional[str]:
        """Get the database column name."""
        return self._db_column
    
    @property
    def db_required(self) -> bool:
        """Whether the field is required."""
        return self._db_required
    
    @property
    def db_unique(self) -> bool:
        """Whether the field should be unique."""
        return self._db_unique
    
    @property
    def db_index(self) -> bool:
        """Whether the field should be indexed."""
        return self._db_index
    
    @property
    def db_check(self) -> Optional[str]:
        """Get the CHECK constraint if any."""
        return self._db_check

    @property
    @abstractmethod
    def db_type(self) -> DBType:
        """Get the database type."""
        raise NotImplementedError("Subclasses must implement db_type")

    def get_column_creation_query(self) -> str:
        """Generate the column definition SQL."""
        parts = [f"{self.db_type.value}"]
        
        # Add constraints
        if self._default is not None:
            if isinstance(self._default, str):
                parts.append(f"DEFAULT '{self._default}'")
            else:
                parts.append(f"DEFAULT {self._default}")
        
        if self.db_unique:
            parts.append("UNIQUE")
            
        if self.db_required:
            parts.append("NOT NULL")
            
        if self.db_check:
            parts.append(f"CHECK ({self.db_check})")
            
        return " ".join(parts)
    
    def get_index_creation_query(self, table_name: str, column_name: str) -> Optional[str]:
        """Generate index creation SQL if needed."""
        if self.db_index:
            index_name = f"idx_{table_name}_{column_name}"
            return f"CREATE INDEX {index_name} ON {table_name} ({column_name})"
        return None
    
    def is_auto(self) -> bool:
        """Whether the field is auto-generated."""
        return False

class PrimaryKey(DatabaseFieldBase, fields.Integer):
    """Auto-incrementing primary key field."""
    
    def __init__(self, big: bool = False, **kwargs):
        """Initialize primary key field."""
        kwargs['required'] = True
        DatabaseFieldBase.__init__(self, **kwargs)
        fields.Integer.__init__(self, **kwargs)
        self._big = big

    @property
    def db_type(self) -> DBType:
        return DBType.BIGSERIAL if self._big else DBType.SERIAL
    
    def get_column_creation_query(self) -> str:
        return f"{self.db_type.value} PRIMARY KEY"
    
    def is_auto(self) -> bool:
        return True

class Integer(DatabaseFieldBase, fields.Integer):
    """Integer field."""
    
    def __init__(self, big: bool = False, small: bool = False, **kwargs):
        """Initialize integer field."""
        if big and small:
            raise ValueError("Field cannot be both big and small")
        DatabaseFieldBase.__init__(self, **kwargs)
        fields.Integer.__init__(self, **kwargs)
        self._big = big
        self._small = small

    @property
    def db_type(self) -> DBType:
        if self._big:
            return DBType.BIGINT
        if self._small:
            return DBType.SMALLINT
        return DBType.INTEGER

class Text(DatabaseFieldBase, fields.String):
    """Text field for storing strings of any length."""
    
    def __init__(self, **kwargs):
        DatabaseFieldBase.__init__(self, **kwargs)
        fields.String.__init__(self, **kwargs)

    @property
    def db_type(self) -> DBType:
        return DBType.TEXT

class Varchar(DatabaseFieldBase, fields.String):
    """Variable-length string field with maximum length."""
    
    def __init__(self, length: int, **kwargs):
        """Initialize varchar field."""
        self._length = length
        DatabaseFieldBase.__init__(self, **kwargs)
        fields.String.__init__(self, **kwargs)

    @property
    def db_type(self) -> DBType:
        return DBType.VARCHAR
    
    def get_column_creation_query(self) -> str:
        parts = [f"{self.db_type.value}({self._length})"]
        
        if self._default is not None:
            parts.append(f"DEFAULT '{self._default}'")
        if self.db_unique:
            parts.append("UNIQUE")
        if self.db_required:
            parts.append("NOT NULL")
        if self.db_check:
            parts.append(f"CHECK ({self.db_check})")
            
        return " ".join(parts)
    
    def _validate(self, value):
        if value is not None and len(value) > self._length:
            raise ValidationError(f"String too long (max {self._length} characters)")
        return super()._validate(value)

class Boolean(DatabaseFieldBase, fields.Boolean):
    """Boolean field."""
    
    def __init__(self, **kwargs):
        DatabaseFieldBase.__init__(self, **kwargs)
        fields.Boolean.__init__(self, **kwargs)

    @property
    def db_type(self) -> DBType:
        return DBType.BOOLEAN

class Numeric(DatabaseFieldBase, fields.Decimal):
    """Decimal number field with fixed precision and scale."""
    
    def __init__(self, 
                 precision: Optional[int] = None,
                 scale: Optional[int] = None,
                 **kwargs):
        """Initialize numeric field."""
        self._precision = precision
        self._scale = scale
        DatabaseFieldBase.__init__(self, **kwargs)
        fields.Decimal.__init__(self, **kwargs)

    @property
    def db_type(self) -> DBType:
        return DBType.NUMERIC
    
    def get_column_creation_query(self) -> str:
        type_def = self.db_type.value
        if self._precision is not None:
            if self._scale is not None:
                type_def += f"({self._precision},{self._scale})"
            else:
                type_def += f"({self._precision})"
                
        parts = [type_def]
        
        if self._default is not None:
            parts.append(f"DEFAULT {self._default}")
        if self.db_unique:
            parts.append("UNIQUE")
        if self.db_required:
            parts.append("NOT NULL")
        if self.db_check:
            parts.append(f"CHECK ({self.db_check})")
            
        return " ".join(parts)

class ForeignKey(DatabaseFieldBase, fields.Integer):
    """Foreign key reference to another table."""
    
    def __init__(self,
                 ref_schema: Union[Type, str],  # Can be class or string for self-reference
                 on_delete: str = "",
                 on_update: str = "",
                 **kwargs):
        """Initialize foreign key field."""
        # Initialize base classes first
        DatabaseFieldBase.__init__(self, **kwargs)
        fields.Integer.__init__(self, **kwargs)
        
        # Store initialization parameters
        self._ref_schema_raw = ref_schema
        self._on_delete = on_delete
        self._on_update = on_update
        
        # These will be set when bind() is called
        self._ref_schema = None
        self._ref_table_name = None
        self.pk_name = None
        self.pk_field = None

    def _bind_to_schema(self, schema_class: Any, *args, **kwargs) -> None:
        """Bind the foreign key to its owner schema class."""
        from .base_schema import BaseSchema
        
        _ref = self._ref_schema_raw
        if isinstance(_ref, str):
            if _ref == 'self':
                _ref = schema_class
            else:
                raise ValueError("String references other than 'self' are not supported")
                
        if not issubclass(_ref, BaseSchema):
            raise ValueError("ref_schema must be a subclass of BaseSchema")
            
        self._ref_schema = _ref
        self._ref_table_name = self._ref_schema._table()
        self.pk_name, self.pk_field = self._ref_schema._get_pk()
        
        if not self.pk_name:
            raise ValueError(f"Referenced schema {_ref.__name__} has no primary key")
        if not self.pk_field:
            raise ValueError(f"Referenced schema {_ref.__name__} has no primary key field")

    @property
    def db_type(self) -> DBType:
        if self.pk_field is None:
            return DBType.INTEGER
        return DBType.INTEGER if isinstance(self.pk_field, PrimaryKey) else self.pk_field.db_type
    
    def get_column_creation_query(self) -> str:
        parts = [
            f"{self.db_type.value}",
            f"REFERENCES {self._ref_table_name}({self.pk_name})"
        ]
        
        if self._on_delete:
            parts.append(f"ON DELETE {self._on_delete.upper()}")
        if self._on_update:
            parts.append(f"ON UPDATE {self._on_update.upper()}")
        if self.db_unique:
            parts.append("UNIQUE")
        if self.db_required:
            parts.append("NOT NULL")
            
        return " ".join(parts)

class Date(DatabaseFieldBase, fields.Date):
    """Date field."""
    
    def __init__(self, **kwargs):
        DatabaseFieldBase.__init__(self, **kwargs)
        fields.Date.__init__(self, **kwargs)

    @property
    def db_type(self) -> DBType:
        return DBType.DATE

class Time(DatabaseFieldBase, fields.Time):
    """Time field."""
    
    def __init__(self, **kwargs):
        DatabaseFieldBase.__init__(self, **kwargs)
        fields.Time.__init__(self, **kwargs)

    @property
    def db_type(self) -> DBType:
        return DBType.TIME

class Timestamp(DatabaseFieldBase, fields.DateTime):
    """Timestamp field with optional auto-update on insert/update."""
    
    def __init__(self,
                 auto_now: bool = False,
                 auto_now_add: bool = False,
                 allow_none: bool = True,
                 **kwargs):
        """Initialize timestamp field."""
        self._auto_now = auto_now
        self._auto_now_add = auto_now_add
        DatabaseFieldBase.__init__(self, **kwargs)
        fields.DateTime.__init__(self, allow_none=allow_none, **kwargs)

    @property
    def db_type(self) -> DBType:
        return DBType.TIMESTAMP
    
    def _serialize(self, value: Any, attr: str, obj: Any, **kwargs) -> Optional[str]:
        """Convert datetime to string."""
        if value is None:
            return None
        return value.isoformat() if isinstance(value, datetime) else str(value)
    
    def _deserialize(self, value: Any, attr: str, data: Dict, **kwargs) -> Optional[datetime]:
        """Convert string to datetime."""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        try:
            if isinstance(value, str):
                return datetime.fromisoformat(value)
        except (TypeError, ValueError) as error:
            raise ValidationError('Not a valid datetime.') from error
        return value
    
    def get_column_creation_query(self) -> str:
        parts = [self.db_type.value]
        
        if self._auto_now or self._auto_now_add:
            parts.append("DEFAULT CURRENT_TIMESTAMP")
            
        if self.db_unique:
            parts.append("UNIQUE")
        if self.db_required:
            parts.append("NOT NULL")
            
        return " ".join(parts)
    
    def is_auto(self) -> bool:
        return self._auto_now or self._auto_now_add
    
    def get_trigger_sql(self, table_name: str, column_name: str) -> Optional[str]:
        """Generate trigger SQL for auto-updating timestamp."""
        if self._auto_now:
            func_name = f"{table_name}_{column_name}_update_timestamp"
            trigger_name = f"trigger_{func_name}"
            return f"""
                CREATE OR REPLACE FUNCTION {func_name}()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.{column_name} = CURRENT_TIMESTAMP;
                    RETURN NEW;
                END;
                $$ language 'plpgsql';

                DROP TRIGGER IF EXISTS {trigger_name} ON {table_name};
                CREATE TRIGGER {trigger_name}
                    BEFORE UPDATE ON {table_name}
                    FOR EACH ROW
                    EXECUTE FUNCTION {func_name}();
            """
        return None

class JSON(DatabaseFieldBase, fields.Dict):
    """JSON field for storing arbitrary JSON data."""
    
    def __init__(self, binary: bool = True, **kwargs):
        """Initialize JSON field."""
        self._binary = binary
        DatabaseFieldBase.__init__(self, **kwargs)
        fields.Dict.__init__(self, **kwargs)

    @property
    def db_type(self) -> DBType:
        return DBType.JSONB if self._binary else DBType.JSON

class Array(DatabaseFieldBase):
    """Array field for storing lists of values."""

    def __init__(
        self,
        item_field: DatabaseFieldBase,
        dimensions: int = 1,
        column=None,
        required=False,
        unique=False,
        index=False,
        default=None,
        check=None,
        **kwargs
    ):
        # 1) Set up the inner marshmallow List field
        self._list_field = fields.List(item_field, **kwargs)

        # 2) Initialize DatabaseFieldBase for DB-related parameters
        super().__init__(
            column=column,
            required=required,
            unique=unique,
            index=index,
            default=default,
            check=check,
            allow_none=kwargs.get('allow_none', False),
        )
        self._dimensions = dimensions
        self._item_field = item_field

    @property
    def container(self):
        """Return the nested field for consistency with your codebase."""
        return self._item_field

    @property
    def db_type(self) -> DBType:
        return DBType.ARRAY

    def serialize(self, value, attr, obj, **kwargs):
        """Delegate Marshmallow serialization to the underlying List field."""
        return self._list_field.serialize(value, attr, obj, **kwargs)
    
    def deserialize(self, value, attr, data, **kwargs):
        """Delegate Marshmallow deserialization to the underlying List field."""
        return self._list_field.deserialize(value, attr, data, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        """Delegate Marshmallow serialization to the underlying List field."""
        return self._list_field._serialize(value, attr, obj, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        """Delegate Marshmallow deserialization to the underlying List field."""
        return self._list_field._deserialize(value, attr, data, **kwargs)

    def get_column_creation_query(self) -> str:
        item_type = self._item_field.db_type.value
        array_suffix = "[]" * self._dimensions
        parts = [f"{item_type}{array_suffix}"]

        if self.db_unique:
            parts.append("UNIQUE")
        if self.db_required:
            parts.append("NOT NULL")
        if self.db_check:
            parts.append(f"CHECK ({self.db_check})")

        return " ".join(parts)
