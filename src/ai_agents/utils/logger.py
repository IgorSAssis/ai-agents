import logging
import sys
from typing import Optional


class Logger:
    _initialized = False

    @classmethod
    def setup(cls, level: str = "INFO") -> None:
        if cls._initialized:
            return

        logging.basicConfig(
            level=getattr(logging, level.upper(), logging.INFO),
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )

        cls._initialized = True

    @classmethod
    def get_logger(cls, name: Optional[str] = None) -> logging.Logger:
        return logging.getLogger(name)
