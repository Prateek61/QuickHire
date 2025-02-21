from typing import Annotated, Dict, Any, Generator, Optional

from pydantic import BaseModel
from fastapi import Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
from fastapi import Header, FastAPI
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

security = HTTPBearer()

async def get_token_from_header(
    authorization: HTTPAuthorizationCredentials = Security(security),
) -> Optional[str]:
    """Extract JWT token from the Authorization header"""
    if not authorization:
        return None
    
    if not authorization or not authorization.scheme.lower() == "bearer":
        return None
    
    credentials = authorization.credentials
    if not credentials:
        return None
        
    return credentials

# Dependency
SessionDep = Annotated[DBSession, Depends(get_session)]
TokenDep = Annotated[Optional[str], Depends(get_token_from_header)]
