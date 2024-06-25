from enum import Enum, auto
from typing import Dict, FrozenSet, List

from plaid.model.institution import Institution as PlaidInstitution


class InstitutionType(Enum):
    NOT_SPECIFIED = auto()
    CASH = auto()
    CREDIT = auto()
    INVESTMENT = auto()

    _INSTITUTION_TO_PRODUCT_MAP: Dict[str, str] = {
        "CASH": "assets",
        "CREDIT": "liabilities",
        "INVESTMENT": "investments",
    }

    @classmethod
    def from_str(cls, institution_type: str) -> "InstitutionType":
        institution_type: str = institution_type.lower()
        if institution_type == "cash":
            return cls.CASH
        if institution_type == "credit":
            return cls.CREDIT
        if institution_type == "investment":
            return cls.INVESTMENT
        return cls.NOT_SPECIFIED

    def to_product(self) -> str:
        if self.name == "NOT_SPECIFIED":
            raise ValueError("Cannot convert unspecified InstitutionType enum to product")
        return InstitutionType._INSTITUTION_TO_PRODUCT_MAP[self.name]


class Institution:

    def __init__(self, name: str, products: List[str], institution_types: FrozenSet[InstitutionType]) -> None:
        self.name = name
        self.products = products
        self.institution_types = institution_types

    @classmethod
    def from_plaid_institution(cls, plaid_institution: PlaidInstitution) -> "Institution":
        institution_types: List[InstitutionType] = []
        if "investments" in plaid_institution.products:
            institution_types.append(InstitutionType.INVESTMENT)
        if "liabilities" in plaid_institution.products:
            institution_types.append(InstitutionType.CREDIT)
        if "assets" in plaid_institution.products:
            institution_types.append(InstitutionType.CASH)

        return cls(
            name=plaid_institution.name,
            products=plaid_institution.products,
            institution_type=frozenset(institution_types),
        )
