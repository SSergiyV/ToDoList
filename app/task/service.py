from app.task.repository import TaskRepository
from app.task.models import Task
from app.task.schemas import TaskCreate, TaskUpdate
from app.task.exceptions import TaskNotFoundError


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def get_all(
        self,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "id",
        order: str = "asc",
        done: bool | None = None,
        search: str | None = None
    ):
        items, total = self.repository.get_all(
        skip,
        limit,
        sort_by,
        order,
        done,
        search
    )

        return {
            "items": items,
            "total": total,
            "skip": skip,
            "limit": limit
        }

    def create(self, data: TaskCreate):
        task = Task(
            title=data.title,
            done=False
        )
        return self.repository.create(task)

    def get_by_id(self, task_id: int):
        task = self.repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFoundError()

        return task

    def update(self, task_id: int, data: TaskUpdate):
        task = self.repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFoundError()

        updates = data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            if value is not None:
                setattr(task, field, value)

        return self.repository.update(task)


    def delete(self, task_id: int):
        task = self.repository.get_by_id(task_id)

        if task is None:
            raise TaskNotFoundError()

        self.repository.delete(task)
        return task