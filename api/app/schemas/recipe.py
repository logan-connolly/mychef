from typing import Optional

from pydantic import BaseModel, AnyUrl


# shared properties
class RecipeBase(BaseModel):
    name: Optional[str]
    url: Optional[AnyUrl]
    image: Optional[AnyUrl]


# properties to receive on item creation
class RecipeCreate(RecipeBase):
    name: str
    url: AnyUrl
    image: AnyUrl


# properties to receive on item update
class RecipeUpdate(RecipeBase):
    pass


# properties hared by models stored in DB
class RecipeDBBase(RecipeBase):
    id: int
    name: str
    url: str
    image: str

    class Config:
        orm_mode = True


# properties to return to client
class RecipeDB(RecipeDBBase):
    pass
