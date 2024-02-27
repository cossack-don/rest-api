from pydantic import BaseModel
from typing import Optional


class Schema_Model_Table_ONE(BaseModel):
    id: int
    category_name: Optional[str] = None

    class Config:
        orm_mode = True