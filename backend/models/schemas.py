from database import *

class UsersSchema(BaseSchema):
    id = F.PrimaryKey()
    username = F.Varchar(255, required=True)
    password_hash = F.Text(required=True)
    email = F.Text(required=True)
    phone_no = F.Text()

class SkillsSchema(BaseSchema):
    id = F.PrimaryKey()
    name = F.Text(required=True)
    category = F.Varchar(50, required=True)
    description = F.Text()

class ProfessionalsSchema(BaseSchema):
    id = F.PrimaryKey()
    user_id = F.ForeignKey(UsersSchema, on_delete='cascade', required=True)
    skill_id = F.ForeignKey(SkillsSchema, on_delete='cascade', required=True)
    cover_letter = F.Text()
    experience = F.Integer()
    hourly_rate = F.Integer()
    availability = F.Text()

class HiresSchema(BaseSchema):
    id = F.PrimaryKey()
    client_id = F.ForeignKey(UsersSchema, on_delete='cascade', required=True)
    professional_id = F.ForeignKey(UsersSchema, on_delete='cascade', required=True)
    skill_id = F.ForeignKey(SkillsSchema, on_delete='cascade', required=True)
    start_date = F.Date()
    end_date = F.Date()
    total_cost = F.Integer()
    status = F.Varchar(50)

class ReviewsSchema(BaseSchema):
    id = F.PrimaryKey()
    hire_id = F.ForeignKey(HiresSchema, on_delete='cascade', required=True)
    professional_id = F.ForeignKey(UsersSchema, on_delete='cascade', required=True)
    client_id = F.ForeignKey(UsersSchema, on_delete='cascade', required=True)
    rating = F.Integer()
    comment = F.Text()
