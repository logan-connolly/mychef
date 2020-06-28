from typing import List

import spacy
from loguru import logger


class IngredientExtractor:
    """Named entity recognizer trained to identify ingredients"""

    def __init__(self, path: str = None):
        self.path = path
        self.nlp = self._load_nlp()

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(path='{self.path}')"

    def _load_nlp(self):
        if self.path:
            logger.debug(f"Loading model from '{self.path}'")
            return spacy.load(self.path)
        logger.warning("Loading blank spacy model.")
        return spacy.blank("en")

    def extract(self, text: str) -> List[str]:
        tokens = self.nlp(text)
        ingredient_set = {token.text for token in tokens.ents}
        return list(ingredient_set)
