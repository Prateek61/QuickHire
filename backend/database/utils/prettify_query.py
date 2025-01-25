import sqlparse

def prettify_sql_query(query: str) -> str:
    return sqlparse.format(query, reindent = True)
