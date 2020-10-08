from typing import Optional

from pydantic import BaseModel


class IngredientBase(BaseModel):
    "Shared properties across all schemas"
    ingredient: Optional[str]


class IngredientCreate(IngredientBase):
    "Properties to receive on item creation"
    ingredient: str


class IngredientUpdate(IngredientBase):
    "Properties needed to update data in DB"
    pass


class IngredientDBBase(IngredientBase):
    "Properties shared by models stored in DB"
    id: int
    ingredient: str

    class Config:
        orm_mode = True


class IngredientDB(IngredientDBBase):
    "Properties to return to client"
    pass
