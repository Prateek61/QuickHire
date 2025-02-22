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
        last_name="Poudel",
        profile_pic_url="data:image/jpeg;base64,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"
    ),
    UserData(
        username="Malenia",
        email="maleniakhatri@gmail",
        password_hash=create_password_hash("password222"),
        phone_no="9841234568",
        first_name="Malenia",
        last_name="Khatri",
        profile_pic_url="https://miro.medium.com/v2/resize:fit:400/1*B8c1ED3QV_yaa6PAWqDgMw.png"
    ),
    UserData(
        username="john",
        email="johndoe@gmail.com",
        password_hash=create_password_hash("password333"),
        phone_no="9841234569",
        profile_pic_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqMFVc0af6Vxc8UKBootbFQJPfPF-mKyM0hg&s"
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
        status="completed",
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