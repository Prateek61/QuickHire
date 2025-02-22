# 🔥 QuickHire Custom ORM Documentation

## 📖 Overview

The QuickHire ORM is a powerful, type-safe Object-Relational Mapper built specifically for PostgreSQL. It provides a declarative way to define database schemas and models with robust field types, relationships, and an expressive query builder.

## 🎯 Key Features

- 🏗️ **Schema-based Models**: Define tables using declarative schemas with type validation
- 🔍 **Fluent Query Builder**: Build complex SQL queries with an intuitive interface
- 🔗 **Auto-Join Detection**: Automatic relationship detection for JOINs
- 🛠️ **Rich Field Types**: Comprehensive set of field types with validation
- 📝 **Auto Migrations**: Automatic table creation and schema management

## 📚 Usage Guide

### Schema Definition Examples

Here are real examples from the QuickHire project:

```python
from database.model import BaseSchema, fields

class Users(BaseSchema):
    __data_class__ = UserData  # Link to dataclass for type safety

    id = fields.PrimaryKey()
    username = fields.Text(required=True, unique=True)
    email = fields.Text(required=True, unique=True)
    phone_no = fields.Text(required=True, unique=True)
    password_hash = fields.Text(required=True)
    first_name = fields.Varchar(50, required=False)
    last_name = fields.Varchar(50, required=False)
    is_active = fields.Boolean(default=True, required=True)
    updated_at = fields.Timestamp(auto_now=True)
    created_at = fields.Timestamp(auto_now_add=True)

    # Table-level indexes and constraints
    __table_args__ = (
        Index('username', 'email', name='idx_user_lookup'),
        Index('last_login', method='brin')  # BRIN index for timestamps
    )

class Professionals(BaseSchema):
    __data_class__ = ProfessionalData

    id = fields.PrimaryKey()
    user_id = fields.ForeignKey(Users, required=True, on_delete='cascade')
    skill_id = fields.ForeignKey(Skills, required=True, on_delete='cascade')
    title = fields.Text(required=True)
    experience = fields.Integer(required=True)
    hourly_rate = fields.Numeric(required=True)
    location = fields.Text(required=True)
    is_available = fields.Boolean(default=True, required=True)
    updated_at = fields.Timestamp(auto_now=True)
    created_at = fields.Timestamp(auto_now_add=True)

    __table_args__ = (
        Index('user_id', 'skill_id', name='idx_professional_lookup'),
        Index('location', name='idx_professional_location')
    )
```

### Real Query Examples

#### 1. Complex Join Query with Column Aliases

This example from the professionals API shows how to fetch professional data with related user and skill information:

```python
def get_professional_query():
    return Select(
        Users,
        *Professionals.all_cols("p_"),  # Prefix professional columns with p_
        *Skills.all_cols("s_"),         # Prefix skill columns with s_
        *Users.all_cols("u_")           # Prefix user columns with u_
    ).join(Professionals).join(Skills)   # Auto-detects relationships
```

#### 2. Multiple Joins with Conditions

From the hires API, showing how to join multiple tables with specific conditions:

```python
query = Select(
    Hires,
    Hires.all_cols(),
    Users.col("username"),
    Professionals.col("title"),
    Users.col("location"),
    Skills.col("name")
).join(Professionals).join(Skills).join(
    Users, 
    Condition().eq(Users.col("id"), Professionals.col("user_id"))
).where(
    Condition().eq(Hires.col("client_id"), user_id)
).get_query()
```

#### 3. Complex Data Processing

Example of processing joined data from multiple tables:

```python
# Raw query execution
results = QueryHelper.fetch_multiple_raw(query, session)

# Process results with column prefixes
processed_data = [
    HireResponse(
        professional_username=item.pop("username"),
        professional_title=item.pop("title"),
        professional_location=item.pop("location"),
        skill_name=item.pop("name"),
        hire=HireData(**item)
    )
    for item in results
]
```

### Query Builder Features

#### 1. Conditions

```python
# Simple condition
condition = Condition().eq(Users.col("is_active"), True)

# Complex conditions
condition = (
    Condition()
    .eq(Hires.col("status"), "pending")
    .and_()
    .gt(Professionals.col("hourly_rate"), 50)
    .and_()
    .ilike(Users.col("username"), "%john%")
)
```

#### 2. Joins with Auto-Detection

```python
# Auto-detected join based on foreign keys
query = (
    Select(Users)
    .join(Professionals)  # Uses user_id foreign key automatically
    .join(Skills)        # Uses skill_id foreign key automatically
)

# Manual join condition
query = (
    Select(Users)
    .join(
        Professionals,
        Condition().eq(Users.col("id"), Professionals.col("user_id")),
        join_type="LEFT"
    )
)
```

#### 3. Column Selection and Aliases

```python
query = Select(
    Users,
    Users.col("username", "user_name"),     # With alias
    Professionals.col("title", "job_title"), # With alias
    Statement.count(Reviews.col("id"), "review_count")  # Aggregate
)
```

### Working with Data

#### 1. Creating Records

```python
# Create a professional profile
professional = ProfessionalData(
    user_id=user.id,
    skill_id=skill.id,
    title="Senior Carpenter",
    experience=5,
    hourly_rate=45.00,
    location="New York"
)

try:
    new_prof = QueryHelper.insert([professional], Professionals, session)[0]
    session.commit()
except Exception as e:
    session.rollback()
    raise HTTPException(status_code=500, detail="Failed to create professional")
```

#### 2. Querying Records

```python
# Get professional with joins
query = (
    Select(
        Users,
        Professionals.col("id"),
        Professionals.col("title"),
        Users.col("username"),
        Users.col("location"),
        Skills.col("name")
    )
    .join(Professionals)
    .join(Skills)
    .where(
        Condition().eq(Professionals.col("id"), prof_id)
    )
    .limit(1)
    .get_query()
)

result = QueryHelper.fetch_one_raw(query, session)
```

#### 3. Updating Records

```python
# Update hire status
hire.status = "completed"
update_query = hire.get_update_query()
QueryHelper.run(update_query, session)
session.commit()
```

### Check Constraints

Using the Hires model as an example:

```python
class Hires(BaseSchema):
    __table_args__ = (
        CheckConstraint('total_hours >= 0', name='check_total_hours'),
        CheckConstraint('total_amount >= 0', name='check_total_amount'),
        CheckConstraint('start_date <= end_date', name='check_date_range'),
        CheckConstraint(
            "status in ('pending', 'active', 'completed', 'cancelled')"
        )
    )
```

### Best Practices

1. Always use transactions:
```python
try:
    # Your operations here
    session.commit()
except Exception as e:
    session.rollback()
    raise HTTPException(status_code=500, detail=str(e))
```

2. Use prefixed column names in joins:
```python
Select(
    Users,
    *Professionals.all_cols("p_"),  # Clear prefix for professional fields
    *Skills.all_cols("s_")          # Clear prefix for skill fields
)
```

3. Leverage automatic join detection:
```python
# Let the ORM detect relationships
query = Select(Users).join(Professionals).join(Skills)
```

4. Use appropriate indexes:
```python
__table_args__ = (
    Index('user_id', 'skill_id', name='idx_professional_lookup'),
    Index('location', name='idx_professional_location')
)
```

5. Implement proper constraints:
```python
class Reviews(BaseSchema):
    __table_args__ = (
        CheckConstraint('rating >= 0 AND rating <= 5', name='check_rating'),
        Index('hire_id', 'professional', 'client', name='idx_review_lookup')
    )
```

## 🐛 Error Handling

1. Handle database errors:
```python
try:
    QueryHelper.run(query, session)
    session.commit()
except Exception as e:
    session.rollback()
    logger.error(f"Database error: {e}")
    raise HTTPException(status_code=500, detail="Database error occurred")
```

2. Handle validation errors:
```python
try:
    professional = QueryHelper.insert([prof_data], Professionals, session)[0]
except ValidationError as e:
    raise HTTPException(status_code=400, detail=str(e))
```

3. Handle not found errors:
```python
result = QueryHelper.fetch_one(query, session, UserSchema)
if not result:
    raise HTTPException(status_code=404, detail="User not found")