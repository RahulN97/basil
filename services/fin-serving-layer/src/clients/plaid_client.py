import time
from typing import Any, Callable, List

import plaid
from plaid.api.plaid_api import PlaidApi
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.item_public_token_exchange_response import ItemPublicTokenExchangeResponse
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.link_token_create_response import LinkTokenCreateResponse
from plaid.model.products import Products

from models.institution import InstitutionType
from models.item import ItemAccess
from models.link_token import LinkToken
from utils import settings
from utils.logging import logger


class PlaidClient:

    CLIENT_NAME: str = settings.APP_NAME

    def __init__(self, plaid_env: plaid.Environment, plaid_client_id: str, plaid_secret: str) -> None:
        configuration: plaid.Configuration = plaid.Configuration(
            host=plaid_env,
            api_key={
                "clientId": plaid_client_id,
                "secret": plaid_secret,
            },
        )
        api_client: plaid.ApiClient = plaid.ApiClient(configuration)
        self.client: PlaidApi = PlaidApi(api_client)

    @staticmethod
    def log_action(f: Callable[..., Any]) -> Callable[..., Any]:
        def inner(*args, **kwargs) -> Any:
            start_time: float = time.time()
            result: Any = f(*args, **kwargs)
            logger.info(f"Plaid client action: {f.__name__}, completed in {time.time() - start_time:.4f} seconds")
            return result

        return inner

    @staticmethod
    def _get_products_from_institution_type(institution_type: InstitutionType) -> List[Products]:
        if institution_type == InstitutionType.CASH:
            return [Products("transactions")]
        if institution_type == InstitutionType.CREDIT:
            return [Products("liabilities")]
        if institution_type == InstitutionType.INVESTMENT:
            return [Products("investments")]
        raise Exception(f"Cannot fetch plaid products for institution type: {institution_type}")

    @staticmethod
    def _get_optional_products_from_institution_type(institution_type: InstitutionType) -> List[Products]:
        if institution_type == InstitutionType.CASH:
            return []
        if institution_type == InstitutionType.CREDIT:
            return [Products("transactions")]
        if institution_type == InstitutionType.INVESTMENT:
            return [Products("transactions")]
        raise Exception(f"Cannot fetch optional plaid products for institution type: {institution_type}")

    @log_action
    def create_link_token(self, user_id: str, institution_type: InstitutionType) -> LinkToken:
        products: List[Products] = self._get_products_from_institution_type(institution_type)
        optional_products: List[Products] = self._get_optional_products_from_institution_type(institution_type)
        request: LinkTokenCreateRequest = LinkTokenCreateRequest(
            client_name=self.CLIENT_NAME,
            country_codes=[CountryCode("US")],
            language="en",
            user=LinkTokenCreateRequestUser(client_user_id=user_id),
            products=products,
            optional_products=optional_products,
        )
        response: LinkTokenCreateResponse = self.client.link_token_create(request)

        return LinkToken(token=response.link_token)

    @log_action
    def exchange_public_token(self, public_token: str) -> ItemAccess:
        request: ItemPublicTokenExchangeRequest = ItemPublicTokenExchangeRequest(public_token=public_token)
        response: ItemPublicTokenExchangeResponse = self.client.item_public_token_exchange(request)

        return ItemAccess(access_token=response["access_token"], item_id=response["item_id"])
