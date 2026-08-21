from app.core.security import hash_password
from app.user.exceptions import UserAlreadyExistsError
from app.user.models import User
from app.user.schemas import UserCreate
from app.user.repository import UserRepository

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(self, user_data: UserCreate) -> User:
        email = str(user_data.email)

        if self.repository.get_by_email(email) is not None:
            raise UserAlreadyExistsError()

        user = User(
            email=email,
            password_hash=hash_password(user_data.password),
        )

        return self.repository.create(user)