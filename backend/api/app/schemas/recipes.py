from pydantic import AnyUrl

from app.schemas.base import BaseSchema


class RecipeSchemaBase(BaseSchema):
    """Shared properties of all recipe schemas"""

    name: str
    source_id: int


class InRecipeSchemaRaw(RecipeSchemaBase):
    """Properties to receive on received post request"""

    url: AnyUrl
    image: AnyUrl
    ingredients: str


class InRecipeSchema(RecipeSchemaBase):
    """Properties to receive on item creation"""

    url: str
    image: str
    ingredients: dict[str, list[str]]


class RecipeSchema(InRecipeSchema):
    """Properties to receive on item retrieval"""

    id: int
