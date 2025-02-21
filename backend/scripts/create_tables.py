from base import *
from database import *
from app.models import TABLES
from app.dependencies import load_config

from typing import List, Type

def create_tables(tables: List[Type[BaseSchema]], session: DBSession):
    for table in tables:
        print(f"Creating table: {table.__name__}")
        table.create_table(session)
        print(f"Table created: {table.__name__}")

def main():
    conf = load_config("config.json")
    with DBEngine(config=conf['postgres'], log=conf["db_log"]) as engine:
        with engine.session() as session:
            create_tables(TABLES, session)
    
if __name__ == "__main__":
    main()
