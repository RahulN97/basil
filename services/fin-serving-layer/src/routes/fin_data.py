from fastapi import APIRouter

from dependencies import FinClient
from models.institution import InstitutionType
from models.item import ItemAccess, ItemAccessCreate
from models.link_token import LinkToken, LinkTokenCreate


router: APIRouter = APIRouter()


@router.post("/link_token", response_model=LinkToken)
async def create_link_token(fin_client: FinClient, request: LinkTokenCreate) -> LinkToken:
    return fin_client.create_link_token(
        user_id=request.user_id,
        institution_type=InstitutionType.from_str(request.institution_type),
    )


@router.post("/item_access", response_model=ItemAccess)
async def exchange_public_token(fin_client: FinClient, request: ItemAccessCreate) -> ItemAccess:
    item_access: ItemAccess = fin_client.exchange_public_token(public_token=request.public_token)
    # create db row
    return item_access
