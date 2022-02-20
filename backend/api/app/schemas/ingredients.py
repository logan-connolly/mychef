from app.schemas.base import BaseSchema


class IngredientSchemaBase(BaseSchema):
    """Shared properties across all schemas"""

    ingredient: str


class InIngredientSchema(IngredientSchemaBase):
    """Properties to receive on item creation"""

    ...


class IngredientSchema(IngredientSchemaBase):
    """Properties of ingredient in DB"""

    id: int
