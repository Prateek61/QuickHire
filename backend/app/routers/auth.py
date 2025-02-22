from fastapi import APIRouter, HTTPException, Depends, Security
from pydantic import BaseModel
from typing import Optional
from ..dependencies import SessionDep, TokenDep, Select, Condition, QueryHelper, Statement
from ..models import Users, UserData
from ..utils.create_password_hash import create_password_hash, check_password
from ..utils.jwt import create_jwt_token

from typing import List, Optional

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

class UserCreate(BaseModel):
    username: str
    email: str
    phone_no: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=TokenResponse)
async def register(user: UserCreate, session: SessionDep):
    check_unique_query = Select(Users, Users.col("id")).where(
        Condition().eq(Users.col("username"), user.username).or_()
        .eq(Users.col("email"), user.email)
    ).limit(1).get_query()
    res = QueryHelper.fetch_multiple_raw(check_unique_query, session)

    if len(res) > 0:
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered"
        )
    
    # Create a new user
    password_hash = create_password_hash(user.password)
    user_data = UserData(
        username=user.username,
        email=user.email,
        phone_no=user.phone_no,
        password_hash=password_hash,
        first_name=user.first_name,
        last_name=user.last_name
    )

    try:
        new_user = QueryHelper.insert([user_data], Users, session)[0]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to create user"
        )
    
    # Create access token
    token_data = {"sub": user.username, "id": new_user.id}
    token = create_jwt_token(token_data)

    session.commit()
    return TokenResponse(access_token=token)

@router.post("/login", response_model=TokenResponse)
async def login(user_login: UserLogin, session: SessionDep):
    # Verify credentials
    q = Select(Users).where(
        Condition().eq(Users.col("username"), user_login.username)
    ).limit(1).get_query()
    res: List[UserData] = QueryHelper.fetch_multiple(q, session, Users)

    if len(res) == 0 or not check_password(user_login.password, res[0].password_hash):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    
    # Create access token
    token_data = {"sub": user_login.username, "id": res[0].id}
    token = create_jwt_token(token_data)

    return TokenResponse(access_token=token)

from ..internal.current_user import SafeUser, get_current_user

# Protected route example
@router.get("/me", response_model=SafeUser)
async def get_current_user_info(current_user: SafeUser = Depends(get_current_user)):
    return current_user
