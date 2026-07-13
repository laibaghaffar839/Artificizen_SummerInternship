from fastapi import Depends, APIRouter
from app.security import get_current_user
from app.models import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user