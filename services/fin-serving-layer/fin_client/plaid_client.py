import os
from typing import List, Optional

import plaid
from plaid.api.plaid_api import PlaidApi
from plaid.model.country_code import CountryCode
from plaid.model.credit_account_subtype import CreditAccountSubtype
from plaid.model.credit_account_subtypes import CreditAccountSubtypes
from plaid.model.credit_filter import CreditFilter
from plaid.model.depository_account_subtype import DepositoryAccountSubtype
from plaid.model.depository_account_subtypes import DepositoryAccountSubtypes
from plaid.model.depository_filter import DepositoryFilter
from plaid.model.institutions_get_request import InstitutionsGetRequest
from plaid.model.institutions_get_response import InstitutionsGetResponse
from plaid.model.investment_account_subtype import InvestmentAccountSubtype
from plaid.model.investment_account_subtypes import InvestmentAccountSubtypes
from plaid.model.investment_filter import InvestmentFilter
from plaid.model.link_token_account_filters import LinkTokenAccountFilters
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.link_token_create_response import LinkTokenCreateResponse
from plaid.model.products import Products

from fin_client.base_fin_client import BaseFinClient
from fin_client.model.institution import Institution, InstitutionType
from fin_client.model.link_token import LinkToken


PLAID_ENV_MAP = {
    "sandbox": plaid.Environment.Sandbox,
    "development": plaid.Environment.Development,
    "production": plaid.Environment.Production,
}


class PlaidClient(BaseFinClient):

    CLIENT_NAME = "nw-tracker"

    def __init__(self) -> None:
        plaid_env: Optional[str] = os.getenv("PLAID_ENV")
        plaid_client_id: Optional[str] = os.getenv("PLAID_CLIENT_ID")
        plaid_secret: Optional[str] = os.getenv("PLAID_SECRET")

        host: plaid.Environment = PLAID_ENV_MAP.get(plaid_env, plaid.Environment.Sandbox)
        configuration: plaid.Configuration = plaid.Configuration(
            host=host,
            api_key={
                'clientId': plaid_client_id,
                'secret': plaid_secret,
            },
        )
        api_client: plaid.ApiClient = plaid.ApiClient(configuration)
        self.client: PlaidApi = PlaidApi(api_client)

    def get_institutions(self, institution_type: InstitutionType) -> List[Institution]:
        request: InstitutionsGetRequest = InstitutionsGetRequest(
            count=500, offset=0, country_codes=[CountryCode("US")],
        )
        response: InstitutionsGetResponse = self.client.institutions_get(request)

        institutions: List[Institution] = [Institution(i) for i in response.institutions]
        if institution_type:
            return [i for i in institutions if institution_type in i.institution_types]
        return institutions

    def create_link_token(self, user_id: str, institution_type: InstitutionType) -> LinkToken:
        product = None
        account_filters = None
        if institution_type == InstitutionType.CASH:
            product: Products = Products("assets")
            account_filters: LinkTokenAccountFilters = LinkTokenAccountFilters(
                depository=DepositoryFilter(
                    account_subtypes=DepositoryAccountSubtypes([
                        DepositoryAccountSubtype('checking'),
                        DepositoryAccountSubtype('savings')
                    ])
                ),
            )
        elif institution_type == InstitutionType.CREDIT:
            product = Products("liabilities")
            account_filters = LinkTokenAccountFilters(
                credit=CreditFilter(
                    account_subtypes=CreditAccountSubtypes([CreditAccountSubtype('credit card')])
                ),
            )
        elif institution_type == InstitutionType.INVESTMENT:
            product = Products("investments")
            account_filters = LinkTokenAccountFilters(
                investment=InvestmentFilter(
                    account_subtypes=InvestmentAccountSubtypes([InvestmentAccountSubtype('all')])
                ),
            )

        request: LinkTokenCreateRequest = LinkTokenCreateRequest(
            client_name="basil-fin-serving-layer",
            country_codes=[CountryCode("US")],
            language="en",
            user=LinkTokenCreateRequestUser(user_id),
            products=product,
            account_filters=account_filters,
        )
        response: LinkTokenCreateResponse = self.client.link_token_create(request)

        return LinkToken(token=response.link_token)
