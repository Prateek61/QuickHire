from database import *
from utils import *
from models import *

from typing import List

def print_query(query: Query, session: DBSession):
    print(query.construct_query(session.cursor))

def run_query(query: Query, session: DBSession):
    session.cursor.execute(query.construct_query(session.cursor))

create_tables: bool = False
print_queries: bool = True

def main():
    conf = load_config('config.json')

    tables: List[BaseSchema] = [
        SkillsSchema(),
        UsersSchema(),
        ProfessionalsSchema(),
        HiresSchema(),
        ReviewsSchema()
    ]

    with DBEngine(config=conf['postgres'], autocommit=True) as engine:
        with engine.session() as session:
            for table in tables:
                query = table._get_table_creation_query()

                if print_queries:
                    print_query(query, session)
                if create_tables:
                    run_query(query, session)
                session.commit()

if __name__ == '__main__':
    main()
