from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.user.repository import UserRepository
from app.user.service import UserService


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repository = UserRepository(db)
    return UserService(repository)