from typing import Optional

from pydantic import BaseModel, AnyUrl


# shared properties
class SourceBase(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None


# properties to receive on item creation
class SourceCreate(SourceBase):
    name: str
    url: AnyUrl


# properties hared by models stored in DB
class SourceUpdate(SourceBase):
    pass


# properties hared by models stored in DB
class SourceDBBase(SourceBase):
    id: int
    name: str
    url: str

    class Config:
        orm_mode = True


# properties to return to client
class SourceDB(SourceDBBase):
    pass
