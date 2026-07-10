from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from Task6 import User, get_db
from security import hash_password


app = FastAPI()


# Pydantic Schema
class UserCreate(BaseModel):
    username: str
    password: str



@app.post("/auth/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    # Check existing user
    existing_user = (
        db.query(User)
        .filter(User.username == user.username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    # Hash password
    hashed_password = hash_password(
        user.password
    )


    # Save user
    new_user = User(
        username=user.username,
        password=hashed_password
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return {
        "message": "User created successfully",
        "username": new_user.username
    }