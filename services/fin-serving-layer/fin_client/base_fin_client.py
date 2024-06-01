from abc import ABC, abstractmethod
from typing import List

from fin_client.model.institution import Institution, InstitutionType
from fin_client.model.link_token import LinkToken


class BaseFinClient(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_institutions(self, institution_type: InstitutionType) -> List[Institution]:
        """
        Get a list of supported institutions

        institution_type: institution type to optionally filter on
        """
        pass

    @abstractmethod
    def create_link_token(self, user_id: str, institution_type: InstitutionType) -> LinkToken:
        pass
