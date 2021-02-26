import tarfile
from pathlib import Path

from loguru import logger


class Model:
    """Base class for model object to be attached to application"""

    directory = Path(__file__).parent

    def __init__(self, model_path: str) -> None:
        self.model_path = model_path
        if not self.model_path.is_dir():
            self.untar()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(path='{self.model_path}')"

    def untar(self) -> None:
        """Attempt to untar compressed model object directory"""
        logger.info(f"Attempting to untar model at {str(self.model_path)}.tar.gz")
        with tarfile.open(f"{self.model_path}.tar.gz") as tar:
            tar.extractall(path=self.model_path.parent)
