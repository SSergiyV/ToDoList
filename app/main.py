from fastapi import FastAPI
from app.task.router import router
from app.task.models import Task  # Import the Task model to ensure it's registered with SQLAlchemy
from app.core.exception_handlers import duplicate_task_handler
from app.task.exceptions import DuplicateTaskError


app = FastAPI()

app.include_router(router)

app.add_exception_handler(
    DuplicateTaskError,
    duplicate_task_handler
)
