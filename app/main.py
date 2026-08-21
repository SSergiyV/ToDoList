from fastapi import FastAPI
from app.task.router import router as task_router
from app.user.router import router as auth_router
from app.task.models import Task  # Import the Task model to ensure it's registered with SQLAlchemy
from app.user.models import User  # Import the User model to ensure it's registered with SQLAlchemy
from app.core.exception_handlers import duplicate_task_handler, task_not_found_handler, user_already_exists_handler
from app.task.exceptions import DuplicateTaskError, TaskNotFoundError
from app.user.exceptions import UserAlreadyExistsError


app = FastAPI()

app.include_router(task_router)
app.include_router(auth_router)

app.add_exception_handler(
    DuplicateTaskError,
    duplicate_task_handler
)

app.add_exception_handler(
    TaskNotFoundError,
    task_not_found_handler
)

app.add_exception_handler(
    UserAlreadyExistsError,
    user_already_exists_handler,
)
