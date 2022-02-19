from pydantic import AnyUrl

from app.schemas.base import BaseSchema


class SourceSchemaBase(BaseSchema):
    """Shared properties acrosse all schemas"""

    name: str


class InSourceSchema(SourceSchemaBase):
    """Properties to receive on item creation"""

    url: AnyUrl


class SourceSchema(SourceSchemaBase):
    """Properties shared by models stored in DB"""

    id: int
    url: str
