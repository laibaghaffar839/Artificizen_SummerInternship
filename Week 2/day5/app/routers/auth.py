from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks           #for backgroundtasks task5 day5 
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.security import hash_password, verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

#background function
def welcome_user(username: str):
    print(f"Welcome {username}! Account created successfully.")

# implement backgroundtask here task5 day5
@router.post("/register", response_model=UserResponse)
def register(user:UserCreate,background_tasks: BackgroundTasks, db:Session=Depends(get_db)):
    hashed_password = hash_password(user.password)
    new_user = User(
        username = user.username,
        password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    background_tasks.add_task(
        welcome_user,
        new_user.username
    )

    return new_user

@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == form_data.username
    ).first()


    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )


    if not verify_password(
        form_data.password,
        user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )


    token = create_access_token(
        {
            "sub": user.username,
            "role": user.role
        }
    )


    return {
        "access_token": token,
        "token_type": "bearer"
    }