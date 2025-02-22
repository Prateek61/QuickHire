from fastapi import APIRouter, HTTPException, Depends
from ..dependencies import SessionDep, TokenDep, Select, Condition, QueryHelper, Statement
from ..internal.current_user import UserData, UserDep
from ..models import Reviews, ReviewData, Hires, HireData, Professionals, Users
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)
