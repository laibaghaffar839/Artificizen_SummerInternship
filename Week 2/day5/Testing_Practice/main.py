from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import User
from schemas import UserCreate, UserResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_email = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_email:

        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user

@app.get("/users/me")
def get_me(token: str = None):

    if token is None:

        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    return {
        "message": "Welcome"
    }