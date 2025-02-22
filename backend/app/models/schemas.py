from ..dependencies import *
from dataclasses import dataclass, field
from datetime import datetime

from typing import List

# Typevar which is BaseSchema
T = TypeVar('T', bound=BaseSchema)

@dataclass
class UserData(BaseDataClass):
    username: str
    email: str
    phone_no: str
    password_hash: str = field(default=None)
    id: int = field(default=0)
    first_name: str = field(default=None)
    last_name: str = field(default=None)
    profile_pic_url: str = field(default=None)
    is_active: bool = field(default=True)
    birthday: datetime = field(default=None)
    last_login: datetime = field(default=None)
    updated_at: datetime = field(default=None)
    created_at: datetime = field(default=None)

@dataclass
class ProfessionalData(BaseDataClass):
    user_id: int
    skill_id: int
    title: str
    experience: int
    hourly_rate: float
    location: str
    id: int = field(default=0)
    cover_letter: str = field(default=None)
    is_available: bool = field(default=True)
    updated_at: datetime = field(default=None)
    created_at: datetime = field(default=None)

@dataclass
class SkillData(BaseDataClass):
    name: str
    id: int = field(default=0)
    description: str = field(default=None)

@dataclass
class HireData(BaseDataClass):
    client_id: int
    professional_id: int
    status: str
    start_date: datetime
    end_date: datetime
    total_hours: int
    total_amount: float

    id: int = field(default=0)
    updated_at: datetime = field(default=None)
    created_at: datetime = field(default=None)

@dataclass 
class ReviewData(BaseDataClass):
    hire_id: int
    professional: int
    client: int
    rating: int
    review: str
    
    id: int = field(default=0)
    updated_at: datetime = field(default=None)
    created_at: datetime = field(default=None)

class Users(BaseSchema):
    """User model
    """
    __data_class__ = UserData

    id = PrimaryKey()
    username = Text(required=True, unique=True)
    email = Text(required=True, unique=True)
    phone_no = Text(required=True, unique=True)
    password_hash = Text(required=True)
    first_name = Varchar(50, required=False, allow_none=True)
    last_name = Varchar(50, required=False)
    profile_pic_url = Text(required=False)
    is_active = Boolean(default=True, required=True)
    birthday = Date(required=False)
    updated_at = Timestamp(auto_now=True)
    created_at = Timestamp(auto_now_add=True)
    last_login = Timestamp(auto_now=True)

    # Table-level constraints
    __table_args__ = (
        Index('username', 'email', name='idx_user_lookup'),
        Index('last_login', method='brin')  # BRIN index for timestamps
    )

class Skills(BaseSchema):
    """Skill model
    """
    __data_class__ = SkillData

    id = PrimaryKey()
    name = Text(required=True, unique=True)
    description = Text(required=False)

    __table_args__ = (
        Index('name', name='idx_skill_lookup'),
    )

class Professionals(BaseSchema):
    """Professional model
    """
    __data_class__ = ProfessionalData

    id = PrimaryKey()
    user_id = ForeignKey(Users, required=True, on_delete='cascade')
    skill_id = ForeignKey(Skills, required=True, on_delete='cascade')
    title = Text(required=True)
    experience = Integer(required=True)
    cover_letter = Text(required=False)
    hourly_rate = Numeric(required=True)
    is_available = Boolean(default=True, required=True)
    location = Text(required=True)
    updated_at = Timestamp(auto_now=True)
    created_at = Timestamp(auto_now_add=True)

    __table_args__ = (
        Index('user_id', 'skill_id', name='idx_professional_lookup'),
        Index('location', name='idx_professional_location'),
    )

class Hires(BaseSchema):
    """Hire model
    """

    __data_class__ = HireData

    id = PrimaryKey()
    client_id = ForeignKey(Users, required=True, on_delete='cascade')
    professional_id = ForeignKey(Professionals, required=True, on_delete='cascade')
    status = Text(required=True)
    start_date = Date(required=True)
    end_date = Date(required=True)
    total_hours = Integer(required=True)
    total_amount = Numeric(required=True)

    updated_at = Timestamp(auto_now=True)
    created_at = Timestamp(auto_now_add=True)

    __table_args__ = (
        Index('client_id', 'professional_id', name='idx_hire_lookup'),
        Index('status', name='idx_hire_status'),
        Index('start_date', 'end_date', name='idx_hire_date_range'),
        CheckConstraint('total_hours >= 0', name='check_total_hours'),
        CheckConstraint('total_amount >= 0', name='check_total_amount'),
        CheckConstraint('start_date <= end_date', name='check_date_range'),
        CheckConstraint(
            "status in ('pending', 'active', 'completed', 'cancelled')"
        )
    )

class Reviews(BaseSchema):
    """Review model
    """

    __data_class__ = ReviewData

    id = PrimaryKey()
    hire_id = ForeignKey(Hires, required=True, on_delete='cascade')
    professional =  ForeignKey(Professionals, required=True, on_delete='cascade')
    client = ForeignKey(Users, required=True, on_delete='cascade')
    rating = Integer(required=True)
    review = Text(required=False)
    updated_at = Timestamp(auto_now=True)
    created_at = Timestamp(auto_now_add=True)

    __table_args__ = (
        CheckConstraint('rating >= 0 AND rating <= 5', name='check_rating'),
        Index('hire_id', 'professional', 'client', name='idx_review_lookup'),
        Index('rating', name='idx_review_rating')
    )

TABLES: List[T] = [Users, Skills, Professionals, Hires, Reviews]
