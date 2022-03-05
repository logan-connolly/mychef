from pathlib import Path

import spacy

MODEL_PATH = Path(__file__).parent / "version" / "v1"


class IngredientExtractor:
    """Named entity recognizer trained to identify ingredients"""

    def __init__(self):
        """On initialization, load the spacy model from disk"""
        self.nlp = self._load_model()

    def _load_model(self):
        """Load Spacy model from disk (typing not available spacy<3.0)"""
        assert MODEL_PATH.exists(), "Could not find ingredient model locally"
        return spacy.load(MODEL_PATH)

    def extract(self, text: str) -> list[str]:
        """Extract ingredient entities from text"""
        tokens = self.nlp(text)
        ingredient_set = {token.lemma_.lower() for token in tokens.ents}
        return list(ingredient_set)
