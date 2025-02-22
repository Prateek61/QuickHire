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
        password_hash=create_password_hash("password111"),
        phone_no="9841234567",
        first_name="Prateek",
        last_name="Poudel"
    ),
    UserData(
        username="Malenia",
        email="maleniakhatri@gmail",
        password_hash=create_password_hash("password222"),
        phone_no="9841234568",
        first_name="Malenia",
        last_name="Khatri"
    ),
    UserData(
        username="john",
        email="johndoe@gmail.com",
        password_hash=create_password_hash("password333"),
        phone_no="9841234569",
    )
]

skills: List[SkillData] = [
    SkillData(
        name="plumber",
        description="Pipe fitting, soldering, leak detection, blueprint reading, drainage system installation, and maintenance"
    ),
    SkillData(
        name="Electrician",
        description="Wiring installation, circuit troubleshooting, safety regulations, use of electrical tools, and electrical systems maintenance"
    ),
    SkillData(
        name="Carpenter",
        description="Wood cutting, joinery, furniture making, blueprint reading, polishing and finishing, and furniture repair"
    ),
    SkillData(
        name="Cook",
        description="Knife skills, food preparation, cooking techniques, hygiene & safety, food presentation, and menu planning"
    )
]

professionals: List[ProfessionalData] = [
    ProfessionalData(
        user_id=0,
        skill_id=2,
        title="Senior Carpenter",
        experience=3,
        hourly_rate=50,
        location="Kathmandu",
        cover_letter="I am a professional carpenter with 3 years of experience in furniture making and repair. I have worked on various projects and have a good understanding of joinery, wood cutting, and furniture polishing. I am skilled in blueprint reading and can work on custom furniture projects. I am looking for opportunities to work on new projects and expand my skills."
    ),
    ProfessionalData(
        user_id=2,
        skill_id=3,
        title="Master Cook",
        experience=8,
        hourly_rate=100,
        location="Pokhara",
        cover_letter="I am a professional cook with 8 years of experience in the culinary industry. I have worked in various restaurants and hotels, specializing in different cuisines. I have a passion for cooking and creating new dishes. I am skilled in knife techniques, food preparation, and menu planning. I am looking for opportunities to showcase my skills and create delicious meals for clients."
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
        total_amount=50 * 40
    )
]

reviews: List[ReviewData] = [
    ReviewData(
        hire_id=0,
        professional=0,
        client=1,
        rating=4,
        review="The carpenter did a great job on my furniture project. He was professional, skilled, and completed the work on time. I would recommend him to others."
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