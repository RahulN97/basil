import traceback

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler
from starlette.middleware.cors import CORSMiddleware
from uvicorn.main import ASGIApplication

from api import api_router
from config.app_config import AppConfig
from dependencies import get_app_config
from middleware import LogPerformanceMiddleware
from utils import settings
from utils.logging import logger


def create_app() -> ASGIApplication:
    async def log_stacktrace(request: Request, exc: Exception) -> Response:
        msg: str = f"Error on request: {request.url}"
        logger.error(msg, exc_info=traceback.format_exc())
        return await http_exception_handler(request, exc)

    app: FastAPI = FastAPI(title=settings.APP_NAME)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LogPerformanceMiddleware)
    app.add_exception_handler(HTTPException, log_stacktrace)
    app.include_router(api_router)
    return app


def start_server(app: ASGIApplication) -> None:
    app_config: AppConfig = get_app_config()
    app_target: ASGIApplication | str = "app:app" if app_config.reload or app_config.num_workers > 1 else app
    uvicorn.run(
        app_target,
        host=app_config.service_host,
        port=app_config.service_port,
        reload=app_config.reload,
        log_config=app_config.log_config,
        log_level=app_config.log_level,
        workers=app_config.num_workers,
    )


app: ASGIApplication = create_app()
if __name__ == "__main__":
    start_server(app)
