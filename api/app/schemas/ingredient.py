from typing import Optional

from pydantic import BaseModel


# shared properties
class IngredientBase(BaseModel):
    ingredient: Optional[str] = None


# properties to receive on item creation
class IngredientCreate(IngredientBase):
    ingredient: str


# properties hared by models stored in DB
class IngredientUpdate(IngredientBase):
    pass


# properties hared by models stored in DB
class IngredientDBBase(IngredientBase):
    id: int
    ingredient: str

    class Config:
        orm_mode = True


# properties to return to client
class IngredientDB(IngredientDBBase):
    pass
