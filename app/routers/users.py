from fastapi import APIRouter, Depends
from app.core.deps import get_current_user

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)

@router.get("/")
def list_users(current_user: str = Depends(get_current_user)):
    return [
        {"id": 1, "username": "admin"},
        {"id": 2, "username": "user1"}
    ]

