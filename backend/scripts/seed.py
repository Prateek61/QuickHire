from ..database import *
from ..models import TABLES
from ..app.dependencies import load_config

def seed(session: DBSession):
    ...

def main():
    conf = load_config("backend/config.json")
    with DBEngine(config=conf['postgres'], log=conf["db_log"]) as engine:
        with engine.session() as session:
            seed(session)
    
if __name__ == "__main__":
    main()