"""
Boot FastApi app
"""

import logging
from urllib.parse import urljoin

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import get_settings


def _setup_cors(p_app: FastAPI) -> None:
    """
    Set all CORS enabled origins
    """
    if get_settings().BACKEND_CORS_ORIGINS:
        p_app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                str(origin) for origin in get_settings().BACKEND_CORS_ORIGINS
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


def _create_app() -> FastAPI:
    app_ = FastAPI(
        title=get_settings().PROJECT_NAME,
        openapi_url=urljoin(f"{get_settings().API_V1_STR}/", "openapi.json"),
        version=get_settings().VERSION,
        docs_url="/swagger",
    )
    app_.include_router(api_router, prefix=get_settings().API_V1_STR)
    _setup_cors(app_)
    return app_


app = _create_app()


app_logger = logging.getLogger("app")
app_logger.parent = logging.getLogger("uvicorn")
app_logger.setLevel(logging.DEBUG)
