import os
from typing import Any, Dict, Optional

import plaid

from config.environment import Env
from config.exceptions import MissingConfigError
from utils.logging import get_log_config


class AppConfig:

    DEFAULT_ENV: Env = Env.DEV
    DEFAULT_SERVICE_HOST: str = "0.0.0.0"
    DEFAULT_SERVICE_PORT: int = 8000

    def __init__(self) -> None:
        # env
        self.env: Env = self._extract_env()

        # uvicorn
        self.service_host: str = self._extract_service_host()
        self.service_port: int = self._extract_service_port()
        self.reload: bool = self._resolve_reload()
        self.log_level: str = self._resolve_log_level()
        self.log_config: Dict[str, Any] = get_log_config(self.log_level)
        self.num_workers: int = self._extract_num_workers()

        # plaid
        self.plaid_client_id: str = self._extract_plaid_client_id()
        self.plaid_secret: str = self._extract_plaid_secret()
        self.plaid_env: plaid.Environment = self._resolve_plaid_env()

    def validate_db_creds(self) -> None:
        var_name: str = "GOOGLE_APPLICATION_CREDENTIALS"
        if not (db_creds_path := os.getenv(var_name)):
            return MissingConfigError(var_name)
        if not os.path.isfile(db_creds_path):
            raise FileNotFoundError(f"Missing firestore credentials file {db_creds_path}")

    @staticmethod
    def _raise_if_missing(val: Optional[str], var_name: str) -> str:
        if val is None:
            raise MissingConfigError(var_name)
        return val

    def _extract_env(self) -> Env:
        return Env.from_str(os.getenv("ENV", self.DEFAULT_ENV))

    def _extract_service_host(self) -> str:
        return os.getenv("SERVICE_HOST", self.DEFAULT_SERVICE_HOST)

    def _extract_service_port(self) -> str:
        return int(os.getenv("SERVICE_PORT", self.DEFAULT_SERVICE_PORT))

    def _extract_plaid_client_id(self) -> str:
        var_name: str = "PLAID_CLIENT_ID"
        return self._raise_if_missing(val=os.getenv(var_name), var_name=var_name)

    def _extract_plaid_secret(self) -> str:
        var_name: str = "PLAID_SECRET"
        return self._raise_if_missing(val=os.getenv(var_name), var_name=var_name)

    def _extract_num_workers(self) -> int:
        if self.env == Env.DEV:
            return 1
        return int(os.getenv("NUM_WORKERS", 1))

    def _resolve_reload(self) -> bool:
        return self.env == Env.DEV

    def _resolve_log_level(self) -> str:
        return "debug" if self.env == Env.DEV else "info"

    def _resolve_plaid_env(self) -> plaid.Environment:
        return plaid.Environment.Production if self.env == Env.PROD else plaid.Environment.Sandbox
