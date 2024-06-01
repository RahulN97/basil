import os
from dataclasses import dataclass


DEFAULT_SERVICE_HOST = "127.0.0.1"
DEFAULT_SERVICE_PORT = "8000"


@dataclass(frozen=True)
class AppConfig:
    service_host: str
    service_port: int


def init_app_config() -> AppConfig:
    return AppConfig(
        service_host=os.getenv("SERVICE_HOST", DEFAULT_SERVICE_HOST),
        service_port=os.getenv("SERVICE_PORT", DEFAULT_SERVICE_PORT),
    )
