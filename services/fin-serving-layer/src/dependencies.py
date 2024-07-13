from typing import Annotated

from fastapi import Depends

from clients.firestore_client import FirestoreClient
from clients.plaid_client import PlaidClient
from config.app_config import AppConfig


_app_config_singleton: AppConfig = AppConfig()


def get_app_config() -> AppConfig:
    return _app_config_singleton


AppConfigDep = Annotated[AppConfig, Depends(get_app_config)]


def get_plaid_client(app_config: AppConfigDep) -> PlaidClient:
    return PlaidClient(
        plaid_env=app_config.plaid_env,
        plaid_client_id=app_config.plaid_client_id,
        plaid_secret=app_config.plaid_secret,
    )


FinClient = Annotated[PlaidClient, Depends(get_plaid_client)]


def get_firestore_client(app_config: AppConfigDep) -> FirestoreClient:
    app_config.validate_db_creds()
    return FirestoreClient()


DbClient = Annotated[FirestoreClient, Depends(get_firestore_client)]
