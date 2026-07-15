from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, Token
from app.security import hash_password, verify_password,create_access_token



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



# Register User

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)

def register_user(user: UserCreate,db: Session = Depends(get_db)):

    # Check existing email

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()


    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )


    # Hash password

    hashed_password = hash_password(user.password)


    # Create user

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user


# Login User

@router.post("/login",response_model=Token)

def login_user(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.email == form_data.username
    ).first()


    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    password_check = verify_password(form_data.password,user.hashed_password)


    if not password_check:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    token = create_access_token(
        data={
            "sub": str(user.id)
        }
    )


    return {
        "access_token": token,
        "token_type": "bearer"
    }