# 🚀 QuickHire Backend

A FastAPI-based backend service for the QuickHire platform that connects professionals with clients for short-term hiring needs.

## 🏗️ Project Structure

```
backend/
├── app/                      # Application package
│   ├── dependencies.py       # FastAPI dependencies
│   ├── internal/            
│   │   └── current_user.py  # User authentication utilities
│   ├── models/              # Data models and schemas
│   │   └── schemas.py
│   ├── routers/             # API route handlers
│   │   ├── auth.py         # Authentication routes
│   │   ├── professionals.py # Professional profile routes
│   │   ├── reviews.py      # Review management
│   │   ├── skills.py       # Skills management
│   │   └── hires.py        # Hiring request management
│   └── utils/              # Utility functions
│       ├── jwt.py         # JWT token handling
│       └── create_password_hash.py
├── database/               # Custom ORM package
│   ├── connection/        # Database connection handling
│   ├── engine/           # Query execution engine
│   ├── model/            # Base models and fields
│   └── query/            # Query building and execution
└── scripts/              # Database management scripts
    ├── create_tables.py  # Table creation script
    └── seed.py          # Sample data seeding
```

## ⚙️ Setup and Installation

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix or MacOS:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `config.json` file based on `config-example.json`:

```json
{
    "postgres": {
        "host": "localhost",
        "port": "5432",
        "user": "postgres",
        "password": "postgres",
        "database": "dbms_proj"
    },
    "db_log": true,
    "jwt_secret": "your-secure-secret-key",
    "jwt_expire_minutes": 30
}
```

### 4. Initialize Database

```bash
# Create database tables
python scripts/create_tables.py

# (Optional) Seed sample data
python scripts/seed.py
```

### 5. Run the Application

```bash
# Run FastAPI development server
fastapi dev app
# The API will be available at http://localhost:8000
```

Access the API documentation at: http://localhost:8000/docs

## 🔐 Authentication

The API uses JWT-based authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-token>
```

### Get Authentication Token

```bash
POST /auth/token
{
    "username": "user@example.com",
    "password": "password123"
}
```

## 📚 API Routes

### Authentication Routes

```bash
POST /auth/register        # Register new user
POST /auth/token          # Get JWT token
GET  /auth/me             # Get current user
```

### Professional Routes

```bash
GET    /professionals             # List all professionals
POST   /professionals            # Create professional profile
GET    /professionals/{id}       # Get professional by ID
GET    /professionals/name/{name} # Get professional by username
```

### Skills Routes

```bash
GET    /skills           # List all skills
POST   /skills           # Create new skill
GET    /skills/{id}      # Get skill by ID
PUT    /skills/{id}      # Update skill
DELETE /skills/{id}      # Delete skill
```

### Hire Request Routes

```bash
POST   /hires                # Create hire request
GET    /hires/professional   # Get requests for professional
GET    /hires/user          # Get requests by user
PUT    /hires/{id}/accept   # Accept hire request
PUT    /hires/{id}/reject   # Reject hire request
PUT    /hires/{id}/complete # Mark request as complete
```

### Reviews Routes

```bash
POST   /reviews            # Create review
GET    /reviews/{prof_id}  # Get reviews for professional
```

## 📦 Database Models

The application uses a custom ORM (see [database documentation](database/README.md)). Key models include:

### Users
- Basic user information and authentication
- Links to professional profiles

### Professionals
- Professional profile information
- Skills and expertise
- Pricing and availability

### Skills
- Available service categories
- Skill descriptions and requirements

### Hire Requests
- Booking and scheduling
- Status tracking
- Payment information

### Reviews
- Feedback and ratings
- Service quality metrics

## 🔒 Security Features

- Password hashing using bcrypt
- JWT-based authentication
- Role-based access control
- Input validation and sanitization
- SQL injection protection
- CORS middleware

## 🐛 Error Handling

The API uses standard HTTP status codes and returns detailed error messages:

```json
{
    "detail": "Error description",
    "code": "ERROR_CODE",
    "timestamp": "2024-02-23T12:00:00Z"
}
```

Common status codes:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## 🧪 Testing

Run tests using pytest:

```bash
pytest
```

## 📝 Development Guidelines

1. Use type hints for all function parameters and return values
2. Follow PEP 8 style guidelines
3. Write docstrings for all functions and classes
4. Add appropriate error handling
5. Include unit tests for new features

## 📦 Dependencies

Key dependencies include:
- FastAPI: Web framework
- Uvicorn: ASGI server
- Pydantic: Data validation
- psycopg2: PostgreSQL adapter
- PyJWT: JWT token handling
- python-jose: JWT/JWE/JWS
- passlib: Password hashing
- python-multipart: Form data parsing
- pytest: Testing framework

## 🤝 Contributing

1. Clone the repository
2. Create a new branch
3. Make your changes
4. Write/update tests
5. Create a pull request