from fastapi import APIRouter
from ..dependencies import Condition, Query

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Hello World!"}