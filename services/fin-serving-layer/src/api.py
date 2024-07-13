from typing import Dict

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from routes.fin_data import router as fin_data_router
from routes.users import router as user_router


api_router: APIRouter = APIRouter()
api_router.include_router(fin_data_router, prefix="/fin-data", tags=["fin-data"])
api_router.include_router(user_router, prefix="/users", tags=["users"])


@api_router.get("/health", response_class=JSONResponse)
async def health() -> Dict[str, str]:
    return {"status": "healthy"}
