from sqlalchemy import select
from sqlalchemy.orm import Session
from app.task.models import Task
from sqlalchemy.exc import IntegrityError
from app.task.exceptions import DuplicateTaskError




class TaskRepository:
    def __init__ (self, db: Session):
        self.db = db

    def get_all(
    self,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    done: bool | None = None
    ):
        query = select(Task)

        if done is not None:
            query = query.where(Task.done == done)

        if sort_by == "id":
            column = Task.id
        elif sort_by == "title":
            column = Task.title
        elif sort_by == "created_at":
            column = Task.created_at
        else:
            column = Task.id

        if order == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

        query = query.offset(skip).limit(limit)

        return self.db.execute(query).scalars().all()

    def create(self, task: Task):
        self.db.add(task)

        try:
            self.db.commit()
            self.db.refresh(task)
            return task

        except IntegrityError as e:
            self.db.rollback()
            raise DuplicateTaskError() from e

    def get_by_id(self, task_id: int):
        return self.db.get(Task, task_id)

    def update(self, task: Task):
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task):
        self.db.delete(task)
        self.db.commit()

        