from typing import Dict, List, Optional, Union

from pydantic import AnyUrl, BaseModel


class RecipeBase(BaseModel):
    "Shared properties of all recipe schemas"
    name: Optional[str]
    url: Optional[Union[str, AnyUrl]]
    image: Optional[Union[str, AnyUrl]]
    ingredients: Optional[Union[str, Dict[str, List[str]]]]


class RecipeAdd(RecipeBase):
    "Properties to receive on received post request"
    name: str
    url: AnyUrl
    image: AnyUrl
    ingredients: str


class RecipeCreate(RecipeBase):
    "Properties to receive on item creation"
    name: str
    url: AnyUrl
    image: AnyUrl
    ingredients: Dict[str, List[str]]


class RecipeUpdate(RecipeBase):
    "Properties to receive on item update"
    pass


class RecipeDBBase(RecipeBase):
    "Properties hared by models stored in DB"
    id: int
    name: str
    url: str
    image: str
    ingredients: Dict[str, List[str]]

    class Config:
        orm_mode = True


class RecipeDB(RecipeDBBase):
    "Properties to return to client"
    pass
