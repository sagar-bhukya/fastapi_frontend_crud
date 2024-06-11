from pydantic import BaseModel
from datetime import datetime

class ItemBase(BaseModel):
    title: str
    description: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    class Config:
        orm_mode = True
