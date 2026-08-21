from app.core.exceptions import AppError

class DuplicateTaskError(AppError):
    """Raised when a task with the same title already exists."""
    pass

class TaskNotFoundError(AppError):
    pass