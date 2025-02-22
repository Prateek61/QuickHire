from fastapi import APIRouter
from . import root, auth, skills, professionals

router = APIRouter()
router.include_router(root.router)
router.include_router(auth.router)
router.include_router(skills.router)
router.include_router(professionals.router)
