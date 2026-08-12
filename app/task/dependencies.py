# from fastapi import Depends
# from sqlalchemy.orm import Session

# from app.db.session import get_db
# from app.task.repository import TaskRepository
# from app.task.service import TaskService


# def get_repository(
#     db: Session = Depends(get_db)
# ):
#     return TaskRepository(db)


# def get_service(
#     repository: TaskRepository = Depends(get_repository)
# ):
#     return TaskService(repository)

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.task.repository import TaskRepository
from app.task.service import TaskService


def get_task_service(
    db: Session = Depends(get_db),
) -> TaskService:
    repository = TaskRepository(db)
    return TaskService(repository)