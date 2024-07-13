import time
from typing import Any, Callable, Optional

from google.cloud import firestore
from google.cloud.firestore import CollectionReference, DocumentSnapshot

from models.user import User
from utils.logging import logger


class FirestoreClient:

    def __init__(self) -> None:
        self.client: firestore.Client = firestore.Client()

    @staticmethod
    def log_action(f: Callable) -> Callable:
        def inner(*args, **kwargs) -> Any:
            start_time: float = time.time()
            result: Any = f(*args, **kwargs)
            logger.info(f"Firestore action: {f.__name__}, completed in {time.time() - start_time:.4f} seconds")
            return result

        return inner

    @log_action
    def upsert_user(self, user: User) -> None:
        col_ref: CollectionReference = self.client.collection("users")
        col_ref.document(user.user_id).set(user.model_dump())

    @log_action
    def get_user(self, user_id: str) -> Optional[User]:
        col_ref: CollectionReference = self.client.collection("users")
        doc: DocumentSnapshot = col_ref.document(user_id).get()
        return User(**doc.to_dict()) if doc.exists else None

    @log_action
    def delete_user(self, user_id: str) -> None:
        col_ref: CollectionReference = self.client.collection("users")
        col_ref.document(user_id).delete()

    def add_item(self) -> None:
        pass

    def get_item(self) -> None:
        pass

    def add_accounts(self) -> None:
        pass

    def get_accounts(self) -> None:
        pass

    def add_transactions(self) -> None:
        pass

    def get_transactions(self) -> None:
        pass
