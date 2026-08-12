from sqlalchemy import select
from sqlalchemy.orm import Session
from app.task.models import Task
from sqlalchemy.exc import IntegrityError
from app.task.exceptions import DuplicateTaskError




class TaskRepository:
    def __init__ (self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 10):
        return (
            self.db.execute(
                select(Task)
                .offset(skip)
                .limit(limit)
            )
            .scalars()
            .all()
        )

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

        