from typing import Annotated, Dict, Any, Generator, Optional
import os

from pydantic import BaseModel
from fastapi import Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
from fastapi import Header, FastAPI
from database import *
import json

def get_database_config() -> Dict[str, Any]:
    # Check for DATABASE_URL first (deployment environment)
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return {"url": database_url}
    
    # Try loading from config file (local development)
    config_path = os.getenv("CONFIG_PATH", "config.json")
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
            return config["postgres"]
    
    # Fallback to environment variables
    return {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "database": os.getenv("POSTGRES_DB", "dbms_proj")
    }

def load_config() -> Dict[str, Any]:
    # Load from config file if available
    config_path = os.getenv("CONFIG_PATH", "config.json")
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    
    # Fallback to environment variables
    return {
        "postgres": get_database_config(),
        "db_log": os.getenv("DB_LOG", "true").lower() == "true",
        "jwt_secret": os.getenv("JWT_SECRET", "your-secure-secret-key"),
        "jwt_expire_minutes": int(os.getenv("JWT_EXPIRE_MINUTES", "30"))
    }
    
config: Dict[str, Any] = {}
engine: DBEngine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine
    global config
    
    # Load main configuration
    config = load_config()
    
    # Initialize database engine with appropriate configuration
    if "url" in config["postgres"]:
        engine = DBEngine(url=config["postgres"]["url"], log=config.get("db_log", False))
    else:
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
