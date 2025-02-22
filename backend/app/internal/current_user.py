from pydantic import BaseModel

from fastapi import HTTPException, Depends
from ..utils.jwt import verify_jwt_token
from typing import Optional
from ..dependencies import SessionDep, TokenDep, Select, Condition, QueryHelper, Security, security
from ..models import Users, UserData

from typing import Annotated

async def get_current_user(session: SessionDep, token: TokenDep) -> UserData:
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    
    payload = verify_jwt_token(token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
    select_query = Select(Users).where(
        Condition().eq(Users.col("username"), payload["sub"])
    ).get_query()

    user: UserData = QueryHelper.fetch_one(select_query, session, Users)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    
    return user

UserDep = Annotated[UserData, Depends(get_current_user)]
