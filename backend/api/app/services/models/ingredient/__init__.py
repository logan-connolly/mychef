import spacy
from loguru import logger

from app.services.models import Model


class IngredientExtractor(Model):
    """Named entity recognizer trained to identify ingredients"""

    def __init__(self):
        model_path = Model.directory / "ingredient" / "version" / "v1"
        super().__init__(model_path)
        self.nlp = spacy.load(self.model_path)
        logger.info("Model successfully loaded")

    def extract(self, text: str) -> list[str]:
        """Extract ingredient entities from text"""
        tokens = self.nlp(text)
        ingredient_set = {token.lemma_.lower() for token in tokens.ents}
        return list(ingredient_set)
