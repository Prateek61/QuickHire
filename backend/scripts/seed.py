from base import *
from database import *
from app.dependencies import load_config
from app.models import *
from app.utils import create_password_hash

from datetime import datetime, timedelta

from typing import List

users: List[UserData] = [
    UserData(
        username="Prateek",
        email="prateekpoudel61@gmail",
        password_hash=create_password_hash("password"),
        phone_no="9841234567",
        first_name="Prateek",
        last_name="Poudel"
    ),
    UserData(
        username="Malenia",
        email="malenia@gmail",
        password_hash=create_password_hash("password"),
        phone_no="9841234568",
        first_name="Malenia",
        last_name="Blade of Miquella"
    ),
    UserData(
        username="Duck",
        email="duck@duckmail.com",
        password_hash=create_password_hash("quack"),
        phone_no="9841234569",
    )
]

skills: List[SkillData] = [
    SkillData(
        name="Waterfowl Dance",
        description="Undodgable dance of the waterfowl, idk bro"
    ),
    SkillData(
        name="Plumbing",
        description="Fixin pipes and dat"
    ),
    SkillData(
        name="Sleepdeprivation",
        description="Professional all-nighter"
    ),
    SkillData(
        name="Quacking",
        description="Quack Quack Motherducker"
    )
]

professionals: List[ProfessionalData] = [
    ProfessionalData(
        user_id=0,
        skill_id=2,
        title="Senior Non-Sleeper",
        experience=3,
        hourly_rate=42,
        location="Remote",
        cover_letter="hmm"
    ),
    ProfessionalData(
        user_id=1,
        skill_id=0,
        title="Duck",
        experience=1,
        hourly_rate=12,
        location="Pond",
        cover_letter="Quack Quack"
    )
]

hire: List[HireData] = [
    HireData(
        client_id=1,
        professional_id=0,
        status="active",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=7),
        total_hours=40,
        total_amount=42 * 40
    )
]

reviews: List[ReviewData] = [
    ReviewData(
        hire_id=0,
        professional=0,
        client=1,
        rating=4,
        review="Damn"
    )
]

def seed(session: DBSession):
    global users, skills, professionals, hire, reviews

    # Insert users
    users = QueryHelper.insert(users, Users, session)
    session.commit()
    # Insert skills
    skils = QueryHelper.insert(skills, Skills, session)
    session.commit()
    # Insert professionals
    # First, we need to get the user ids
    for p in professionals:
        p.user_id = users[p.user_id].id
        p.skill_id = skills[p.skill_id].id
    professionals = QueryHelper.insert(professionals, Professionals, session)
    session.commit()
    # Insert hires
    # First, we need to get the user ids and skill ids
    for h in hire:
        h.client_id = users[h.client_id].id
        h.professional_id = professionals[h.professional_id].id
    hire = QueryHelper.insert(hire, Hires, session)
    session.commit()
    # Insert reviews
    # First, we need to get the hire ids
    for r in reviews:
        r.hire_id = hire[r.hire_id].id
        r.professional = professionals[r.professional].id
        r.client = users[r.client].id
    reviews = QueryHelper.insert(reviews, Reviews, session)
    session.commit()


def main():
    conf = load_config("config.json")
    with DBEngine(config=conf['postgres'], log=conf["db_log"]) as engine:
        with engine.session() as session:
            seed(session)
    
if __name__ == "__main__":
    main()