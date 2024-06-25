import os
from typing import Optional

import plaid

from config.exceptions import MissingConfigError


class AppConfig:

    DEFAULT_ENV = "dev"
    DEFAULT_SERVICE_HOST = "0.0.0.0"
    DEFAULT_SERVICE_PORT = "8000"

    def __init__(self) -> None:
        # env
        self.env: str = self._extract_env()

        # service config
        self.service_host: str = self._extract_service_host()
        self.service_port: int = self._extract_service_port()

        # plaid
        self.plaid_client_id: str = self._extract_plaid_client_id()
        self.plaid_secret: str = self._extract_plaid_secret()
        self.plaid_env: plaid.Environment = self._get_plaid_env(self.env)

    @staticmethod
    def _raise_if_missing(val: Optional[str], var_name: str) -> str:
        if val is None:
            raise MissingConfigError(var_name)
        return val

    def _extract_env(self) -> str:
        return os.getenv("ENV", self.DEFAULT_ENV)

    def _extract_service_host(self) -> str:
        return os.getenv("SERVICE_HOST", self.DEFAULT_SERVICE_HOST)

    def _extract_service_port(self) -> str:
        return os.getenv("SERVICE_PORT", self.DEFAULT_SERVICE_PORT)

    def _extract_plaid_client_id(self) -> str:
        var_name: str = "PLAID_CLIENT_ID"
        return self._raise_if_missing(val=os.getenv(var_name), var_name=var_name)

    def _extract_plaid_secret(self) -> str:
        var_name: str = "PLAID_SECRET"
        return self._raise_if_missing(val=os.getenv(var_name), var_name=var_name)

    def _get_plaid_env(self, service_env: str) -> plaid.Environment:
        if service_env == "prod":
            return plaid.Environment.Production
        return plaid.Environment.Sandbox
