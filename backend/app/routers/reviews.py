from fastapi import APIRouter, HTTPException, Depends
from ..dependencies import SessionDep, TokenDep, Select, Condition, QueryHelper, Statement
from ..internal.current_user import UserData, UserDep
from ..models import Reviews, ReviewData, Hires, HireData, Professionals, Users
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)

class ReviewCreate(BaseModel):
    hire_id: int
    rating: int
    review: Optional[str] = None

class ReviewResponse(BaseModel):
    id: int
    hire_id: int
    rating: int
    reviewer_name: str
    reviewer_profile_pic: Optional[str] = None
    review: Optional[str] = None

@router.post("/create", response_model=ReviewResponse)
async def create_review(
    review_req: ReviewCreate,
    user: UserDep,
    session: SessionDep
):
    # Check if the hire exists
    hire_query = Select(
        Hires
    ).where(
        Condition().eq(Hires.col("id"), review_req.hire_id)
    ).limit(1).get_query()
    hire = QueryHelper.fetch_one(hire_query, session, Hires)
    if not hire:
        raise HTTPException(
            status_code=404,
            detail="Hire not found"
        )
    
    # Check if the hire is completed
    if hire.status != "completed":
        raise HTTPException(
            status_code=400,
            detail="Hire is not completed"
        )
    
    # Check if the review already exists
    review_query = Select(Reviews).where(
        Condition().eq(Reviews.col("hire_id"), review_req.hire_id)
    ).limit(1).get_query()
    review = QueryHelper.fetch_one(review_query, session, Reviews)
    if review:
        raise HTTPException(
            status_code=400,
            detail="Review already exists"
        )
    
    review_data = ReviewData(
        hire_id=review_req.hire_id,
        rating=review_req.rating,
        review=review_req.review
    )

    try:
        new_review = QueryHelper.insert([review_data], Reviews, session)[0]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to create review"
        )
    session.commit()

    return ReviewResponse(
        id=new_review.id,
        hire_id=new_review.hire_id,
        rating=new_review.rating,
        reviewer_name=user.username,
        review=new_review.review,
        reviewer_profile_pic=user.profile_pic_url
    )

@router.get("/professional_reviews", response_model=List[ReviewResponse])
async def get_professional_reviews(
    user: UserDep,
    session: SessionDep
):
    query = Select(
        Reviews,
        Reviews.all_cols(),
        Users.col("username"),
        Users.col("profile_pic_url")
    ).join(Hires).join(Professionals).join(Users).where(
        Condition().eq(Professionals.col("user_id"), user.id)
    ).get_query()

    res = QueryHelper.fetch_multiple_raw(query, session)

    return [
        ReviewResponse(
            id=r['id'],
            hire_id=r['hire_id'],
            rating=r['rating'],
            reviewer_name=r['username'],
            reviewer_profile_pic=r['profile_pic_url'],
            review=r['review']
        ) for r in res
    ]
