from typing import Type

from app.db.dal.base import BaseDAL
from app.db.tables.recipes import Recipe
from app.schemas.recipes import InRecipeSchema, RecipeSchema


class RecipesDAL(BaseDAL[InRecipeSchema, RecipeSchema, Recipe]):
    @property
    def _schema(self) -> Type[RecipeSchema]:
        return RecipeSchema

    @property
    def _table(self) -> Type[Recipe]:
        return Recipe
