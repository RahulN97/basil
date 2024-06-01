from typing import Dict

import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

from app_config import AppConfig, init_app_config
from fin_client.base_fin_client import BaseFinClient
from fin_client.model.institution import InstitutionType
from fin_client.model.link_token import LinkToken
from fin_client.provider import provide_fin_client


app: FastAPI = FastAPI()
app_config: AppConfig = init_app_config()
fin_client: BaseFinClient = provide_fin_client()


@app.post("/create/link/token", response_class=JSONResponse)
async def create_link_token(
    user_id: str = Query(..., description="User ID"),
    institution_type: str = Query(..., description="Institution Type"),
) -> Dict[str, str]:
    link_token: LinkToken = fin_client.create_link_token(
        user_id=user_id,
        institution_type=InstitutionType.from_str(institution_type),
    )
    return {"link_token": link_token.token}


@app.get("/institutions/get")
async def get_institutions(access_token: str) -> Dict:
    pass


@app.get("/health", response_class=JSONResponse)
async def health() -> Dict[str, str]:
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host=app_config.service_host, port=app_config.service_port)
