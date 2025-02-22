from fastapi import APIRouter, HTTPException, Depends
from ..dependencies import SessionDep, TokenDep, Select, Condition, QueryHelper, Statement
from ..internal.current_user import UserData, UserDep
from ..models import Professionals, ProfessionalData, Users, UserData, Skills, SkillData, Reviews
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
    professional: ProfessionalData
    user: UserData
    skill: SkillData
    avg_rating: Optional[float] = None

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
        *Professionals.all_cols("p_"),
        *Skills.all_cols("s_"),
        *Users.all_cols("u_"),
        Statement("AVG", Reviews.col("rating"), "avg_rating")
    ).join(Professionals).join(Skills).join(Reviews, Condition().eq(Reviews.col("professional"), Professionals.col("id")), "LEFT")\
    .group_by(Professionals.col("id"), Skills.col("id"), Users.col("id"))

def deserialize_professionals_data(data: List[Dict[str, Any]]) -> List[ProfessionalResponse]:
    user_schema = Users(exclude=["password_hash"])
    prof_schema = Professionals()
    skill_schema = Skills()

    res = []

    for item in data:
        user_data = user_schema.load(
            {key.replace("u_", ""): value for key, value in item.items() if key.startswith("u_") and key != "u_password_hash"}
        )
        prof_data = prof_schema.load(
            {key.replace("p_", ""): value for key, value in item.items() if key.startswith("p_")}
        )
        skill_data = skill_schema.load(
            {key.replace("s_", ""): value for key, value in item.items() if key.startswith("s_")}
        )
        avg_rating = item.get("avg_rating", None)

        res.append(
            ProfessionalResponse(professional=prof_data, user=user_data, skill=skill_data, avg_rating=avg_rating)
        )

    return res

@router.get("/", response_model=List[ProfessionalResponse])
async def get_professionals(session: SessionDep):
    query = get_professional_query().get_query().set_end()

    res = QueryHelper.fetch_multiple_raw(query, session)

    return deserialize_professionals_data(res)

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

    user.password_hash = None
    return ProfessionalResponse(
        professional=new_prof,
        user=user,
        skill=skill
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

    return deserialize_professionals_data([res])[0]

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

    return deserialize_professionals_data([res])[0]
