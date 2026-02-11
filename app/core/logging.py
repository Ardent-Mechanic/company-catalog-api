import logging.config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / "logs"


def setup_logging() -> None:
    LOG_DIR.mkdir(exist_ok=True)

    logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
