from typing import Optional, Union

from pydantic import BaseModel, AnyUrl


class SourceBase(BaseModel):
    "Shared properties acrosse all schemas"
    name: Optional[str]
    url: Optional[Union[str, AnyUrl]]


class SourceCreate(SourceBase):
    "Properties to receive on item creation"
    name: str
    url: AnyUrl


class SourceUpdate(SourceBase):
    "Properties needed to update data in DB"
    pass


class SourceDBBase(SourceBase):
    "Properties shared by models stored in DB"
    id: int
    name: str
    url: str

    class Config:
        orm_mode = True


class SourceDB(SourceDBBase):
    "Properties to return to client"
    pass
