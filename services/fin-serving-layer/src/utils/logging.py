import logging
from typing import Any, Dict

import yaml


def get_log_config(log_level: str) -> Dict[str, Any]:
    log_level: str = log_level.upper()

    with open("utils/logging.yaml", "r") as f:
        log_config: Dict[str, Any] = yaml.safe_load(f)

    for logger in ("", "uvicorn.access", "uvicorn.error"):
        log_config["loggers"][logger]["level"] = log_level

    return log_config


logger: logging.Logger = logging.getLogger()
