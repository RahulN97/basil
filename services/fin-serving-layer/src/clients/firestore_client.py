import time
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional

from google.cloud import firestore
from google.cloud.firestore import CollectionReference, DocumentSnapshot

from models.account import Account
from models.item import Item
from models.transaction import Transaction
from models.user import User
from utils.logging import logger


class DocumentNotFoundError(Exception):
    def __init__(self, id: str, col: str) -> None:
        msg: str = f"Document with id: {id} not found in collection: {col}."
        super().__init__(msg)


class FirestoreClient:

    def __init__(self) -> None:
        self.client: firestore.Client = firestore.Client()
        self.users_col: CollectionReference = self.client.collection("users")
        self.items_col: CollectionReference = self.client.collection("items")
        self.accounts_col: CollectionReference = self.client.collection("accounts")
        self.transactions_col: CollectionReference = self.client.collection("transactions")

    @staticmethod
    def log_action(f: Callable) -> Callable:
        def inner(*args, **kwargs) -> Any:
            start_time: float = time.time()
            result: Any = f(*args, **kwargs)
            logger.info(f"Firestore action: {f.__name__}, completed in {time.time() - start_time:.4f} seconds")
            return result

        return inner

    @log_action
    def save_user(self, user: User) -> None:
        self.users_col.document(user.user_id).set(user.model_dump())

    @log_action
    def get_user(self, user_id: str) -> Optional[User]:
        doc: DocumentSnapshot = self.users_col.document(user_id).get()
        return User(**doc.to_dict()) if doc.exists else None

    @log_action
    def delete_user(self, user_id: str) -> None:
        self.users_col.document(user_id).delete()

    def _update_user_with_item_id(self, user_id: str, item_id: str) -> None:
        user: Optional[User] = self.get_user(user_id)
        if user is None:
            raise DocumentNotFoundError(id=user_id, col="users")
        if item_id not in user.item_ids:
            user.item_ids.append(item_id)
            self.save_user(user)

    @log_action
    def access_token_exists(self, user_id: str, access_token: str) -> bool:
        user: User = self.get_user(user_id)
        if user is None or not user.item_ids:
            return False

        for item_id in user.item_ids:
            item: Item = self.get_item(item_id)
            if item.access_token == access_token:
                return True

        return False

    @log_action
    def save_item(self, item: Item, update_user: bool = True) -> None:
        self.items_col.document(item.item_id).set(item.model_dump())
        if update_user:
            self._update_user_with_item_id(user_id=item.user_id, item_id=item.item_id)

    @log_action
    def get_item(self, item_id: str) -> Optional[Item]:
        doc: DocumentSnapshot = self.items_col.document(item_id).get()
        return Item(**doc.to_dict()) if doc.exists else None

    @log_action
    def delete_item(self, item_id: str) -> None:
        self.items_col.document(item_id).delete()

    def _update_items_with_account_ids(self, accounts: List[Account]) -> None:
        item_to_accounts: Dict[str, List[str]] = defaultdict(list)
        for a in accounts:
            item_to_accounts[a.item_id].append(a.account_id)
        for item_id, account_ids in item_to_accounts:
            item: Optional[Item] = self.get_item(item_id)
            if item is None:
                raise DocumentNotFoundError(id=item_id, col="items")
            item.account_ids = list(set(item.account_ids + account_ids))
            self.save_item(item, update_user=False)

    @log_action
    def save_accounts(self, accounts: List[Account], update_items: bool = True) -> None:
        for a in accounts:
            self.accounts_col.document(a.account_id).set(a.model_dump())
        if update_items:
            self._update_items_with_account_ids(accounts)

    @log_action
    def get_account(self, account_id: str) -> Optional[Account]:
        pass

    @log_action
    def delete_accounts(self, account_ids: List[str]) -> None:
        pass

    def _update_accounts_with_transaction_ids(self, transactions: List[Transaction]) -> None:
        account_to_transactions: Dict[str, List[str]] = defaultdict(list)
        for t in transactions:
            account_to_transactions[t.account_id].append(t.transaction_id)
        for account_id, transaction_ids in account_to_transactions:
            account: Optional[Account] = self.get_account(account_id)
            if account is None:
                raise DocumentNotFoundError(id=account_id, col="accounts")
            account.transaction_ids = list(set(account.transaction_ids + transaction_ids))
            # TODO: save accounts
            # self.save_accounts

    @log_action
    def save_transactions(self, transactions: List[Transaction], update_accounts=True) -> None:
        for t in transactions:
            self.transactions_col.document(t.transaction_id).set(t.model_dump())
        if update_accounts:
            self._update_accounts_with_transaction_ids(transactions)

    @log_action
    def get_transaction(self, transaction_id: str) -> Transaction:
        pass

    @log_action
    def delete_transactions(self, transaction_ids: List[str]) -> None:
        # delete from account as well
        pass
