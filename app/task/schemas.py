from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    model_config = ConfigDict(str_strip_whitespace=True)

class TaskResponse(BaseModel):
    id: int
    title: str
    done: bool
    created_at: datetime  # Use str to represent datetime in ISO format

    model_config = ConfigDict(from_attributes=True)

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None