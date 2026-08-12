from app.task.repository import TaskRepository
from app.task.models import Task
from app.task.schemas import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def get_all(
    self,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc"
):
        return self.repository.get_all(
            skip,
            limit,
            sort_by,
            order
        )

    def create(self, data: TaskCreate):
        task = Task(
            title=data.title,
            done=False
        )
        return self.repository.create(task)

    def get_by_id(self, task_id: int):
        return self.repository.get_by_id(task_id)

    def update(self, task_id: int, data: TaskUpdate):
        task = self.repository.get_by_id(task_id)

        if task is None:
            return None

        if data.title is not None:
            task.title = data.title

        if data.done is not None:
            task.done = data.done

        return self.repository.update(task)


    def delete(self, task_id: int):
        task = self.repository.get_by_id(task_id)

        if task is None:
            return None

        self.repository.delete(task)
        return task