from fastapi import APIRouter
from . import root, auth

router = APIRouter()
router.include_router(root.router)
router.include_router(auth.router)