import tarfile
from pathlib import Path
from typing import List

import spacy
from loguru import logger

from app.core.config import settings


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
        if not self.path:
            return None
        if not self.path.is_dir():
            logger.debug(f"Extracting tar.gz file from '{self.path}'")
            self._untar()
        logger.debug(f"Loading model from '{self.path}'")
        return spacy.load(self.path)

    def extract(self, text: str) -> List[str]:
        tokens = self.nlp(text)
        ingredient_set = {token.lemma_.lower() for token in tokens.ents}
        return list(ingredient_set)


def load_model():
    model_dir = Path("/app/app/services/models")
    model = None
    try:
        model = IngredientExtractor(model_dir / settings.API_MODEL)
        logger.info(f"{model} loaded")
    except TypeError:
        logger.warning("No model specified")
    except OSError:
        logger.warning("Could not find model")
    return model
