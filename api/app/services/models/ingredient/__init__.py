from typing import List

import spacy
from loguru import logger

from app.services.models import Model


class IngredientExtractor(Model):
    """Named entity recognizer trained to identify ingredients"""

    def __init__(self, path: str):
        super().__init__(path)
        self.nlp = spacy.load(self.model_path)
        logger.info(f"{path!r} model successfully loaded")

    def extract(self, text: str) -> List[str]:
        """Extract ingredient entities from text"""
        tokens = self.nlp(text)
        ingredient_set = {token.lemma_.lower() for token in tokens.ents}
        return list(ingredient_set)
