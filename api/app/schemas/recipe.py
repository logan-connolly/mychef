from typing import Any, Dict, List, Optional

from pydantic import BaseModel, AnyUrl


# shared properties
class RecipeBase(BaseModel):
    name: Optional[str]
    url: Optional[Any]
    image: Optional[Any]
    ingredients: Optional[Any]


# properties to receive on item creation
class RecipeCreate(RecipeBase):
    name: str
    url: AnyUrl
    image: AnyUrl
    ingredients: Any


# properties to receive on item update
class RecipeUpdate(RecipeBase):
    ingredients: Optional[Dict[str, List[str]]]


# properties hared by models stored in DB
class RecipeDBBase(RecipeBase):
    id: int
    name: str
    url: str
    image: str
    ingredients: Dict[str, List[str]]

    class Config:
        orm_mode = True


# properties to return to client
class RecipeDB(RecipeDBBase):
    pass
