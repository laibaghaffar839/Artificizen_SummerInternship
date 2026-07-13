from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import User
from app.security import require_admin
from app.database import get_db

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)
@router.get("/dashboard")
def admin_dashboard(
    current_user: User = Depends(require_admin)
):
    return current_user


@router.delete("/users/{id}")
def delete_user(
    id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {
        "message":"User deleted"
    }