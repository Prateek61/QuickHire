import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional
from ..dependencies import config

SECRET_KEY = config.get("jwt_secret", "your-secret-key")  # Get from config or use default
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = config.get("jwt_expire_minutes", 30)

def create_jwt_token(data: Dict) -> str:
    """Create a JWT token with the given data"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt_token(token: str) -> Optional[Dict]:
    """Verify a JWT token and return its payload"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None