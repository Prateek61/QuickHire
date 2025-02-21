from typing import Annotated, Dict, Any, Generator

from contextlib import asynccontextmanager
from fastapi import Header, HTTPException, FastAPI
from database import *
import json

def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    with open(config_path) as f:
        return json.load(f)
    
config: Dict[str, Any] = {}
engine: DBEngine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine
    global config
    config = load_config()
    engine = DBEngine(config["postgres"], log=config.get("db_log", False))
    yield
    engine.close()

def get_session() -> Generator[DBSession, None, None]:
    with engine.session() as s:
        yield s
