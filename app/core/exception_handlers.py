from fastapi import Request
from fastapi.responses import JSONResponse

from app.task.exceptions import DuplicateTaskError


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