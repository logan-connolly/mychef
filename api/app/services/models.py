import tarfile
from pathlib import Path
from typing import List

import spacy
from loguru import logger


class IngredientExtractor:
    """Named entity recognizer trained to identify ingredients"""

    def __init__(self, path: str = None):
        self.path = Path(path) if path else None
        self.nlp = self._load_nlp()

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(path='{self.path}')"

    def _untar(self):
        with tarfile.open(f"{self.path}.tar.gz") as tar:
            tar.extractall(path=self.path.parent)

    def _load_nlp(self):
        if self.path is None:
            logger.warning("Loading blank spacy model.")
            return spacy.blank("en")
        if not self.path.is_dir():
            logger.debug(f"Extracting tar.gz file from '{self.path}'")
            self._untar()
        logger.debug(f"Loading model from '{self.path}'")
        return spacy.load(self.path)

    def extract(self, text: str) -> List[str]:
        tokens = self.nlp(text)
        ingredient_set = {token.text.lower() for token in tokens.ents}
        return list(ingredient_set)
