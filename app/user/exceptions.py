from app.core.exceptions import AppError

class UserAlreadyExistsError(AppError):
    """Raised when a user with the same email already exists."""
    pass