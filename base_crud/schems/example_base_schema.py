from typing import Optional
from pydantic import BaseModel


class Base_Schema_CRUD(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    age: Optional[int] = None
    title: Optional[int] = None

    class Config:
        orm_mode = True