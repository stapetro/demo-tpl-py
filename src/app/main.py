"""
Boot FastApi app
"""

import logging
import typing as t

from fastapi import Depends, FastAPI, Request
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.api.api_v1.auth import api_doc_security
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
        openapi_url=None,
        version=get_settings().VERSION,
        docs_url=None,
        redoc_url=None,
    )
    app_.include_router(api_router, prefix=get_settings().API_V1_STR)
    _setup_cors(app_)
    return app_


app = _create_app()


@app.get(
    "/openapi.json",
    include_in_schema=False,
    dependencies=[Depends(api_doc_security)],
)
async def openapi() -> dict[str, t.Any]:
    """
    Route for OpenAPI schema
    :return: Schema
    """
    return app.openapi()


@app.get(
    "/swagger",
    response_class=HTMLResponse,
    include_in_schema=False,
    dependencies=[Depends(api_doc_security)],
)
async def get_swagger_ui(
    request: Request,
) -> HTMLResponse:
    """
    Route for Swagger UI
    :param request: Route request
    :return: Swagger HTML page
    """
    root_path = request.scope.get("root_path", "").rstrip("/")
    openapi_url = root_path + "/openapi.json"
    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title=get_settings().PROJECT_NAME + " - Swagger UI",
    )


@app.get(
    "/redoc",
    response_class=HTMLResponse,
    include_in_schema=False,
    dependencies=[Depends(api_doc_security)],
)
async def get_redoc_ui(
    request: Request,
) -> HTMLResponse:
    """
    Route for ReDoc
    :param request: Route request
    :return: Redoc HTML page
    """
    root_path = request.scope.get("root_path", "").rstrip("/")
    openapi_url = root_path + "/openapi.json"
    return get_redoc_html(
        openapi_url=openapi_url,
        title=get_settings().PROJECT_NAME + " - ReDoc",
    )


app_logger = logging.getLogger("app")
app_logger.parent = logging.getLogger("uvicorn")
app_logger.setLevel(logging.DEBUG)
