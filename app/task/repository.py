from sqlalchemy import select
from sqlalchemy.orm import Session
from app.task.models import Task
from sqlalchemy.exc import IntegrityError
from app.task.exceptions import DuplicateTaskError
from sqlalchemy import func




class TaskRepository:
    def __init__ (self, db: Session):
        self.db = db

    def get_all(
    self,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    done: bool | None = None,
    search: str | None = None
    ):
        query = select(Task)


        if done is not None:
            query = query.where(Task.done == done)

        if search:
            query = query.where(Task.title.ilike(f"%{search}%"))

        count_query = select(func.count()).select_from(query.subquery())
        total = self.db.execute(count_query).scalar_one()
            
        sort_columns = {
            "id": Task.id,
            "title": Task.title,
            "created_at": Task.created_at,
        }

        column = sort_columns[sort_by]

        if order == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

        query = query.offset(skip).limit(limit)

        items = self.db.execute(query).scalars().all()

        return items, total

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
        try:
            self.db.commit()
            self.db.refresh(task)
            return task
        except IntegrityError as e:
            self.db.rollback()
            raise DuplicateTaskError() from e

    def delete(self, task: Task):
        self.db.delete(task)
        self.db.commit()

        