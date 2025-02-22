from fastapi import APIRouter
from . import root, auth, skills, professionals, hires, reviews

router = APIRouter()
router.include_router(root.router)
router.include_router(auth.router)
router.include_router(skills.router)
router.include_router(professionals.router)
router.include_router(hires.router)
router.include_router(reviews.router)
