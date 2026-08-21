from fastapi import APIRouter, Depends, status

from app.user.dependencies import get_user_service
from app.user.schemas import UserCreate, UserResponse
from app.user.service import UserService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return service.register(user_data)