from typing import Dict
from .query import Query

QUERIES: Dict[str, str] = {
    'create_table': f"CREATE TABLE IF NOT EXISTS %(table_name)s ({Query.SUBQUERY_PATTERN % 'columns'} {Query.SUBQUERY_PATTERN % 'extra'})",
}