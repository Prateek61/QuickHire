from fastapi import APIRouter
from ..dependencies import SessionDep, QueryHelper, Select
from ..models import Skills, SkillData
from pydantic import BaseModel

from typing import List, Any, Optional

router = APIRouter(
    prefix="/skills",
    tags=["skills"]
)

class SkillResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

@router.get("/", response_model=List[SkillResponse])
async def get_skills(session: SessionDep):
    query = Select(Skills).get_query().set_end()
    skills: List[SkillData] = QueryHelper.fetch_multiple(query, session, Skills)

    return [SkillResponse(id=skill.id, name=skill.name, description=skill.description) for skill in skills]
