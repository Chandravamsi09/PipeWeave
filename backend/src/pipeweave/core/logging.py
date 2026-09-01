"""Structured Logger"""
import logging
import sys

def setup_logger(name: str = "pipeweave") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s %(message)s"))
        logger.addHandler(h)
    return logger

logger = setup_logger()
