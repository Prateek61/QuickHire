from fastapi import APIRouter, HTTPException
from ..dependencies import SessionDep, QueryHelper, Select, Condition
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

@router.get("/{skill_id}", response_model=SkillResponse)
async def get_skill(skill_id: int, session: SessionDep):
    query = Select(Skills).where(
        Condition().eq(Skills.col("id"), skill_id)
    ).limit(1).get_query()
    skill: SkillData = QueryHelper.fetch_one(query, session, Skills)

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )
    
    return SkillResponse(id=skill.id, name=skill.name, description=skill.description)

@router.get("/name/{skill_name}", response_model=SkillResponse)
async def get_skill_by_name(skill_name: str, session: SessionDep):
    query = Select(Skills).where(
        Condition().ilike(Skills.col("name"), skill_name)
    ).limit(1).get_query()
    skill: SkillData = QueryHelper.fetch_one(query, session, Skills)

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )
    
    return SkillResponse(id=skill.id, name=skill.name, description=skill.description)

@router.get("/search/{search_query}", response_model=List[SkillResponse])
async def search_skill(search_query: str, session: SessionDep):
    query = Select(Skills).where(
        Condition().ilike(Skills.col("name"), search_query)
    ).get_query()
    skills: List[SkillData] = QueryHelper.fetch_multiple(query, session, Skills)

    return [SkillResponse(id=skill.id, name=skill.name, description=skill.description) for skill in skills]
