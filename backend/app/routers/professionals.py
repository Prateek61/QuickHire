from fastapi import APIRouter
from ..dependencies import SessionDep, TokenDep
from ..models import Professionals, ProfessionalData, Users, UserData
from pydantic import BaseModel

from typing import List, Any

router = APIRouter(
    prefix="/professionals",
    tags=["professionals"]
)

class ProfessionalCreate(BaseModel):
    username: str
