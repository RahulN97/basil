from fin_client.base_fin_client import BaseFinClient
from fin_client.plaid_client import PlaidClient


def provide_fin_client() -> BaseFinClient:
    return PlaidClient()
