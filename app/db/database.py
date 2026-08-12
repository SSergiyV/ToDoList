from app.db.base import Base
from app.db.session import engine
from app.task import models


def create_tables():
    Base.metadata.create_all(bind=engine)