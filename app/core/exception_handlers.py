from fastapi import Request
from fastapi.responses import JSONResponse

from app.task.exceptions import DuplicateTaskError, TaskNotFoundError
from app.user.exceptions import UserAlreadyExistsError


async def duplicate_task_handler(
    request: Request,
    exc: DuplicateTaskError
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": "Task with this title already exists"
        }
    )

async def task_not_found_handler(
    request: Request,
    exc: TaskNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Task not found"
        }
    )

async def user_already_exists_handler(
    request: Request,
    exc: UserAlreadyExistsError,
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": "User with this email already exists"
        },
    )