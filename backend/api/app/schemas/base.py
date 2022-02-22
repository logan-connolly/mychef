from pydantic import BaseModel


class BaseSchema(BaseModel):
    """All pydantic schemas should use ORM"""

    class Config:
        orm_mode = True
