from typing import Dict

QUERIES: Dict[str, str] = {
    'create_table': "CREATE TABLE IF NOT EXISTS %(table_name)s ({{columns}} {{extra}})"
}