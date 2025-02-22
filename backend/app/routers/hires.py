from fastapi import APIRouter, HTTPException, Depends
from ..dependencies import SessionDep, TokenDep, Select, Condition, QueryHelper, Statement
from ..internal.current_user import UserData, UserDep
from ..models import Hires, HireData, Professionals, ProfessionalData, Users, UserData, Skills, SkillData
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

router = APIRouter(
    prefix="/hires",
    tags=["hires"]
)

class HireRequest(BaseModel):
    professional_id: int
    start_date: datetime
    end_date: datetime
    total_hours: int
    total_amount: float

class HireResponse(BaseModel):
    hire: HireData
    professional_username: str
    professional_title: str
    professional_location: str  
    skill_name: str

@router.post("/create", response_model=HireResponse)
async def create_hire(
    hire_req: HireRequest,
    user: UserDep,
    session: SessionDep
):
    # Check if the professional exists
    prof_query = Select(
        Users,
        Professionals.col("id"),
        Professionals.col("title"),
        Users.col("username"),
        Users.col("location"),
        Skills.col("name")
    ).join(Professionals).join(Skills).where(
        Condition().eq(Professionals.col("id"), hire_req.professional_id)
    ).limit(1).get_query()

    prof_data = QueryHelper.fetch_one_raw(prof_query, session)
    if not prof_data:
        raise HTTPException(
            status_code=404,
            detail="Professional not found"
        )
    
    hire = HireData(
        client_id=user.id,
        professional_id=hire_req.professional_id,
        start_date=hire_req.start_date,
        end_date=hire_req.end_date,
        total_hours=hire_req.total_hours,
        status="pending"
    )
    try:
        hire = QueryHelper.insert([hire], Hires, session)[0]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to create hire"
        )

    return HireResponse(
        hire=hire,
        professional_username=prof_data['username'],
        professional_title=prof_data['title'],
        professional_location=prof_data['location'],
        skill_name=prof_data['name']
    )

@router.get("/", response_model=List[HireResponse])
async def my_hires(user: UserDep, session: SessionDep):
    query = Select(
        Hires,
        Hires.all_cols(),
        Users.col("username"),
        Professionals.col("title"),
        Users.col("location"),
        Skills.col("name")
    ).join(Professionals).join(Skills).join(
        Users, Condition().eq(Users.col("id"), Professionals.col("user_id"))
    ).where(
        Condition().eq(Hires.col("client_id"), user.id)
    ).get_query()

    res = QueryHelper.fetch_multiple_raw(query, session)

    return [
        HireResponse(
            professional_username=item.pop("username"),
            professional_title=item.pop("title"),
            professional_location=item.pop("location"),
            skill_name=item.pop("name"),
            hire=HireData(**item)
        )

        for item in res
    ]

@router.post("/cancel")
async def cancel_hire(hire_id: int, user: UserDep, session: SessionDep):
    # Check if the hire exists
    hire_query = Select(Hires).where(
        Condition().eq(Hires.col("id"), hire_id)
    ).limit(1).get_query()
    hire: HireData = QueryHelper.fetch_one(hire_query, session, Hires)

    if not hire:
        raise HTTPException(
            status_code=404,
            detail="Hire not found"
        )
    
    # Check if the hire belongs to the user
    if hire.client_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to cancel this hire"
        )
    
    # Check if the hire is pending
    if hire.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Hire cannot be cancelled"
        )
    
    hire.status = "cancelled"
    # TODO: Update the hire
    session.commit()
    return {"message": "Hire cancelled"}

@router.post("/accept")
async def accept_hire(hire_id: int, user: UserDep, session: SessionDep):
    # Check if the hire exists
    hire_query = Select(Hires).where(
        Condition().eq(Hires.col("id"), hire_id)
    ).limit(1).get_query()
    hire: HireData = QueryHelper.fetch_one(hire_query, session, Hires)

    if not hire:
        raise HTTPException(
            status_code=404,
            detail="Hire not found"
        )
    
    # Check if the hire belongs to the user
    if hire.professional_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to accept this hire"
        )
    
    # Check if the hire is pending
    if hire.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Hire cannot be accepted"
        )
    
    hire.status = "accepted"
    # TODO: Update the hire

    return {"message": "Hire accepted"}

@router.post("/complete")
async def complete_hire(hire_id: int, user: UserDep, session: SessionDep):
    # Check if the hire exists
    hire_query = Select(Hires).where(
        Condition().eq(Hires.col("id"), hire_id)
    ).limit(1).get_query()
    hire: HireData = QueryHelper.fetch_one(hire_query, session, Hires)

    if not hire:
        raise HTTPException(
            status_code=404,
            detail="Hire not found"
        )
    
    # Check if the hire belongs to the user
    if hire.client_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to complete this hire"
        )
    
    # Check if the hire is accepted
    if hire.status != "accepted":
        raise HTTPException(
            status_code=400,
            detail="Hire cannot be completed"
        )
    
    hire.status = "completed"
    # TODO: Update the hire

    return {"message": "Hire completed"}
