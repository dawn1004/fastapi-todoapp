from pydantic import BaseModel
from typing import Optional


class Todo(BaseModel):
    id: Optional[str] = ""
    title: str 
    description: str
    isDone: Optional[bool] = False 