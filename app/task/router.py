from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from app.task.dependencies import get_task_service
from app.task.service import TaskService
from app.task.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.task.exceptions import DuplicateTaskError


router = APIRouter()


@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: TaskService = Depends(get_task_service)
):
    return service.get_all(skip, limit)

@router.post("/tasks", response_model=TaskResponse,  responses={409: {"description": "Task with this title already exists"}})
def create_task(
    data: TaskCreate,
    service: TaskService = Depends(get_task_service)
):
    return service.create(data)

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    task = service.get_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    service: TaskService = Depends(get_task_service)
):
    task = service.update(task_id, data)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    task = service.delete(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {"message": "Task deleted"}