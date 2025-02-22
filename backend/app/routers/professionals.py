from fastapi import APIRouter, HTTPException, Depends
from ..dependencies import SessionDep, TokenDep, Select, Condition, QueryHelper
from ..internal.current_user import UserData, UserDep
from ..models import Professionals, ProfessionalData, Users, UserData, Skills, SkillData
from pydantic import BaseModel

from typing import List, Any, Optional, Dict

router = APIRouter(
    prefix="/professionals",
    tags=["professionals"]
)

class ProfessionalCreate(BaseModel):
    skill_id: int
    title: str
    experience: int
    hourly_rate: float
    location: str
    cover_letter: Optional[str] = None

class ProfessionalResponse(BaseModel):
    id: int
    user_id: int
    username: str
    skill_id: int
    skill_name: str
    skill_description: Optional[str] = None
    title: str
    experience: int
    hourly_rate: float
    location: str
    cover_letter: Optional[str] = None
    is_available: bool

class ProfessionalCreate(BaseModel):
    skill_id: int
    title: str
    experience: int
    hourly_rate: float
    location: str
    cover_letter: Optional[str] = None

def get_professional_query() -> Select:
    return Select(
        Users,
        Professionals.col("id"),
        Professionals.col("user_id"),
        Users.col("username"),
        Professionals.col("skill_id"),
        Professionals.col("title"),
        Professionals.col("experience"),
        Professionals.col("hourly_rate"),
        Professionals.col("location"),
        Professionals.col("cover_letter"),
        Professionals.col("is_available"),
        Skills.col("name", "skill_name"),
        Skills.col("description", "skill_description")
    ).join(Professionals).join(Skills)

@router.get("/", response_model=List[ProfessionalResponse])
async def get_professionals(session: SessionDep):
    query = get_professional_query().get_query().set_end()

    res = QueryHelper.fetch_multiple_raw(query, session)

    return [
        ProfessionalResponse(**item) for item in res
    ]

@router.post("/", response_model=ProfessionalResponse)
async def create_professional(professional: ProfessionalCreate, user: UserDep, session: SessionDep):
    # Check if skill exists
    skill_query = Select(Skills).where(
        Condition().eq(Skills.col("id"), professional.skill_id)
    ).limit(1).get_query()
    skill: SkillData = QueryHelper.fetch_one(skill_query, session, Skills)

    if not skill:
        raise HTTPException(
            status_code=400,
            detail="Skill not found"
        )
    
    # Check if professional already exists
    prof_query = Select(Professionals).where(
        Condition().eq(Professionals.col("user_id"), user.id)
    ).limit(1).get_query()
    prof = QueryHelper.fetch_one(prof_query, session, Professionals)
    if prof:
        raise HTTPException(
            status_code=400,
            detail="Professional already exists"
        )
    
    prof_data = ProfessionalData(
        user_id=user.id,
        skill_id=professional.skill_id,
        title=professional.title,
        experience=professional.experience,
        hourly_rate=professional.hourly_rate,
        location=professional.location,
        cover_letter=professional.cover_letter,
    )

    try:
        new_prof = QueryHelper.insert([prof_data], Professionals, session)[0]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to create professional"
        )
    
    session.commit()

    return ProfessionalResponse(
        id=new_prof.id,
        user_id=new_prof.user_id,
        username=user.username,
        skill_id=new_prof.skill_id,
        skill_name=skill.name,
        skill_description=skill.description,
        title=new_prof.title,
        experience=new_prof.experience,
        hourly_rate=new_prof.hourly_rate,
        location=new_prof.location,
        cover_letter=new_prof.cover_letter,
        is_available=new_prof.is_available
    )

@router.get("/id/{professional_id}", response_model=ProfessionalResponse)
async def get_professional(professional_id: int, session: SessionDep):
    query = get_professional_query().where(
        Condition().eq(Professionals.col("id"), professional_id)
    ).limit(1).get_query()

    res = QueryHelper.fetch_one_raw(query, session)

    if not res:
        raise HTTPException(
            status_code=404,
            detail="Professional not found"
        )

    return ProfessionalResponse(**res)

@router.get("/{professional_name}", response_model=ProfessionalResponse)
async def get_professional_by_name(professional_name: str, session: SessionDep):
    query = get_professional_query().where(
        Condition().ilike(Users.col("username"), professional_name)
    ).limit(1).get_query()

    res = QueryHelper.fetch_one_raw(query, session)

    if not res:
        raise HTTPException(
            status_code=404,
            detail="Professional not found"
        )

    return ProfessionalResponse(**res)
