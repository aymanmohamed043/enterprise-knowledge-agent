"""
Central logging setup. Call configure_logging() from main.py at startup.
"""
import logging
from pathlib import Path

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def configure_logging() -> None:
    """Configure a simple file logger."""
    log_file = Path(__file__).resolve().parents[2] / "app.log"
    logging.basicConfig(
        filename=log_file,
        filemode="a",
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        force=True,
    )


