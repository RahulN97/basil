from enum import Enum, auto
from typing import Dict, FrozenSet, List

from plaid.model.institution import Institution as PlaidInstitution
from pydantic import BaseModel


class InstitutionType(Enum):

    NOT_SPECIFIED = auto()
    CASH = auto()
    CREDIT = auto()
    INVESTMENT = auto()

    @classmethod
    def from_str(cls, institution_type: str) -> "InstitutionType":
        try:
            return cls[institution_type.upper()]
        except KeyError:
            return cls.NOT_SPECIFIED


class Institution(BaseModel):
    name: str
    products: List[str]
    institution_types: FrozenSet[InstitutionType]

    _PRODUCT_TO_INSTITUTION_TYPE: Dict[str, InstitutionType] = {
        "assets": InstitutionType.CASH,
        "liabilities": InstitutionType.CREDIT,
        "investments": InstitutionType.INVESTMENT,
    }

    @classmethod
    def from_plaid_institution(cls, plaid_institution: PlaidInstitution) -> "Institution":
        institution_types: FrozenSet[InstitutionType] = frozenset(
            cls._PRODUCT_TO_INSTITUTION_TYPE[product]
            for product in plaid_institution.products
            if product in cls._PRODUCT_TO_INSTITUTION_TYPE
        )
        return cls(
            name=plaid_institution.name,
            products=plaid_institution.products,
            institution_type=institution_types,
        )
