from fastapi import APIRouter
from ..dependencies import DBSession
from ..models import Users, UserData

router = APIRouter(
    prefix="/auth",
    tags=["auto"]
)

@router.get("/")
async def register(session: DBSession):
    ...
