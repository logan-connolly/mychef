import debugpy
from loguru import logger


def start_debugging_server():
    logger.info("Activating debugging server on port :5678 ...")
    debugpy.listen(("0.0.0.0", 5678))
