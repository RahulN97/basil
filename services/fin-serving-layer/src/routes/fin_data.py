from typing import List

from fastapi import APIRouter

from dependencies import DbClient, FinClient
from models.account import Account
from models.institution import InstitutionType
from models.item import Item, ItemAccess, ItemAccessCreate
from models.link_token import LinkToken, LinkTokenCreate
from models.transaction import RemovedTransaction, Transaction
from routes.common import handle_exceptions
from utils.logging import logger


router: APIRouter = APIRouter()


@router.post("/link_token", response_model=LinkToken)
@handle_exceptions
async def create_link_token(fin_client: FinClient, request: LinkTokenCreate) -> LinkToken:
    return fin_client.create_link_token(
        user_id=request.user_id,
        institution_type=InstitutionType.from_str(request.institution_type),
    )


@router.post("/item_access", response_model=ItemAccess)
@handle_exceptions
async def exchange_public_token(db_client: DbClient, fin_client: FinClient, request: ItemAccessCreate) -> ItemAccess:
    item_access: ItemAccess = fin_client.exchange_public_token(request.public_token)

    if db_client.access_token_exists(user_id=request.user_id, access_token=item_access.access_token):
        logger.info("Access token already exists. No need to fetch data from financial data source.")
        return item_access

    logger.info("Fetching data from financial data source")
    save_item_access(
        db_client=db_client,
        fin_client=fin_client,
        user_id=request.user_id,
        item_access=item_access,
    )

    return item_access


def save_item_access(db_client: DbClient, fin_client: FinClient, user_id: str, item_access: ItemAccess) -> None:
    transactions: List[Transaction]
    removed_transactions: List[RemovedTransaction]
    transactions, removed_transactions = fin_client.get_transactions(item_access=item_access)
    accounts: List[Account] = fin_client.get_accounts(item_access=item_access, transactions=transactions)
    item: Item = Item(
        item_id=item_access.item_id,
        user_id=user_id,
        access_token=item_access.access_token,
        account_ids=[a.account_id for a in accounts],
    )

    try:
        db_client.save_item(item)
        db_client.save_accounts(accounts, update_items=False)
        db_client.save_transactions(transactions, update_accounts=False)
        db_client.delete_transactions([r.transaction_id for r in removed_transactions])
    except Exception as e:
        db_client.delete_item(item_id=item.item_id)
        db_client.delete_accounts(account_ids=[a.account_id for a in accounts])
        db_client.delete_transactions(transaction_ids=[t.transaction_id for t in transactions])
        raise Exception(f"Failed to save transactions, accounts, and item to DB.\nDetails: {str(e)}")


"""
design pattern

api
    -> exchange public token
        if access token exists, get data from firestore
        else, get data from plaid client
    -> get account
        get data from firestore
    -> update account
        get data from plaid client
        store in firestore
        return
"""
