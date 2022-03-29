from typing import Type

from app.db.dal.base import BaseDAL
from app.db.tables.ingredients import Ingredient
from app.schemas.ingredients import IngredientSchema, InIngredientSchema


class IngredientsDAL(BaseDAL[InIngredientSchema, IngredientSchema, Ingredient]):
    @property
    def _schema(self) -> Type[IngredientSchema]:
        return IngredientSchema

    @property
    def _table(self) -> Type[Ingredient]:
        return Ingredient
