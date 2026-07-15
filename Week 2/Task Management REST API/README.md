# Task Management REST API

A secure and modular Task Management REST API built with **FastAPI and PostgreSQL**.

This project is an end-of-week capstone that combines authentication, database relationships, CRUD operations, dependency injection, error handling, and automated testing.

The API allows users to register, login, and manage their own tasks securely using JWT authentication.

---

# Features

## Authentication & Security

- User registration
- Secure password hashing using Bcrypt
- User login with JWT authentication
- Protected routes using JWT tokens
- Users can only access their own tasks

## Task Management

Users can:

- Create tasks
- View all their tasks
- View a single task
- Update tasks
- Delete tasks
- Filter tasks by status

## Additional Features

- PostgreSQL database integration
- SQLAlchemy ORM
- Dependency Injection
- Modular routers
- CORS configuration
- Global JSON exception handling
- Automated API testing using Pytest
- Swagger API documentation

---

# Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic v2
- Passlib (Bcrypt)
- Python-JOSE (JWT)
- Uvicorn
- Pytest
- FastAPI TestClient
- HTTPX

---

# Project Structure

```
Task Management REST API/

│
├── app/
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   └── tasks.py
│   │
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── dependencies.py
│   └── exceptions.py
│
├── tests/
│   ├── conftest.py
│   └── test_api.py
│
├── .env
├── requirements.txt
└── README.md
```

---

# File Description

## database.py

Responsible for:

- PostgreSQL database connection
- Creating SQLAlchemy engine
- Creating database sessions
- Providing `get_db()` dependency


## models.py

Contains SQLAlchemy database models.

### User Model

Fields:

- id
- username
- email
- hashed_password


### Task Model

Fields:

- id
- title
- description
- status
- due_date
- owner_id

The Task model is connected with User using a foreign key relationship.

---

## schemas.py

Contains Pydantic models for:

- Request validation
- Response formatting

Includes:

- UserCreate
- UserResponse
- TaskCreate
- TaskUpdate
- TaskResponse
- Token

---

## security.py

Handles authentication logic:

- Password hashing
- Password verification
- JWT token creation
- JWT token validation

---

## dependencies.py

Contains reusable FastAPI dependencies:

- Database session dependency
- Current authenticated user verification

---

## routers/auth.py

Handles authentication routes:

### Register User

```
POST /auth/register
```

Creates a new user and stores a hashed password.


### Login User

```
POST /auth/login
```
login with email and password (in username box "write email")
Verifies credentials and returns a JWT access token.

---

## routers/tasks.py

Handles task operations:

Routes:

```
POST   /tasks/
GET    /tasks/
GET    /tasks/{task_id}
PUT    /tasks/{task_id}
DELETE /tasks/{task_id}
```

All task routes are protected and require authentication.

---

## main.py

Application entry point.

Responsible for:

- Creating FastAPI application
- Registering routers
- Enabling CORS
- Adding global exception handler
- Creating database tables

---

# Authentication Flow

```
User Registration
        |
        ↓
Password Hashing
        |
        ↓
Save User in Database
        |
        ↓
User Login
        |
        ↓
Verify Password
        |
        ↓
Generate JWT Token
        |
        ↓
Access Protected Routes
```

---

# Authorization

Every task belongs to a specific user.

When a user requests a task:

1. JWT token is verified
2. Current user is identified
3. Task ownership is checked

A user can only view or modify their own tasks.

---

# Running the Project

## 1. Create Virtual Environment

```
python -m venv venv
```

Activate:

Mac/Linux:

```
source venv/bin/activate
```

---

## 2. Install Dependencies

```
pip install -r requirements.txt
```

---

## 3. Environment Variables

Create a `.env` file:

```
DATABASE_URL=your_postgresql_database_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 4. Run Application

```
uvicorn app.main:app --reload
```

Application runs at:

```
http://127.0.0.1:8000
```

---

# Swagger Documentation

FastAPI provides automatic API documentation.

Open:

```
http://127.0.0.1:8000/docs
```

You can test all endpoints directly from Swagger UI.

---

# Testing

Tests are written using Pytest and FastAPI TestClient.

Run:

```
pytest -v
```

Test cases:

| Test | Result |
|---|---|
| Register User | Passed |
| Login User | Passed |
| Create Task | Passed |
| Fetch Tasks | Passed |
| Unauthorized Access | Passed |

---

# Key Concepts Learned

- FastAPI application structure
- JWT authentication
- Password hashing
- Authentication vs Authorization
- SQLAlchemy relationships
- PostgreSQL integration
- Dependency Injection
- CRUD operations
- Router organization
- Exception handling
- CORS configuration
- API testing with Pytest

---

# Summary

This project demonstrates how to build a secure REST API using FastAPI.
It includes user authentication, JWT-based authorization, PostgreSQL database integration, SQLAlchemy ORM, protected CRUD operations, modular routing, error handling, and automated testing.
The project helped in understanding how production-style backend applications are designed, structured, and secured.
