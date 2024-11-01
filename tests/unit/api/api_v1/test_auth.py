# pylint: disable=missing-module-docstring,missing-function-docstring,
# pylint: disable=missing-class-docstring,no-self-use
from unittest import mock

import pytest
from fastapi import HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import SecretStr
from starlette.requests import Request

from app.api.api_v1.auth import ApiDocSecurity

pytestmark = pytest.mark.unit


@pytest.mark.anyio
class TestApiDocSecurity:
    @staticmethod
    @pytest.fixture(scope="class")
    def mock_http_basic_cls() -> HTTPBasic:
        with mock.patch("app.api.api_v1.auth.HTTPBasic") as mock_http_basic:
            yield mock_http_basic

    @pytest.mark.parametrize(
        "env_name,api_doc_enabled,realm",
        [
            ("prd", False, "test-realm"),
            ("tst-loc", None, None),
        ],
    )
    async def test_api_doc_disabled(
        self,
        mock_http_basic_cls: HTTPBasic,
        env_name: str,
        api_doc_enabled: bool,
        realm: str,
    ):
        mock_http_basic_cls.return_value = mock.MagicMock(spec=HTTPBasic, realm=realm)
        mock_request = mock.MagicMock(spec=Request)
        doc_security = ApiDocSecurity(basic=mock_http_basic_cls())

        with mock.patch("app.api.api_v1.auth.get_settings") as mock_get_settings:
            mock_get_settings.return_value = mock.Mock(
                ENV_NAME=env_name, API_DOC_ENABLED=api_doc_enabled
            )
            with pytest.raises(HTTPException):
                _ = await doc_security(mock_request)

    async def test_api_doc_enabled__dev_env(
        self,
        mock_http_basic_cls: HTTPBasic,
    ):
        mock_http_basic_cls.return_value = mock.MagicMock(spec=HTTPBasic, realm=None)
        mock_request = mock.MagicMock(spec=Request)
        doc_security = ApiDocSecurity(basic=mock_http_basic_cls())

        with mock.patch("app.api.api_v1.auth.get_settings") as mock_get_settings:
            mock_get_settings.return_value = mock.Mock(
                ENV_NAME="tst-loc", API_DOC_ENABLED=True
            )
            current_user_name = await doc_security(mock_request)

        assert current_user_name is None

    async def test_api_doc_enabled__prd_env_no_credentials(
        self,
        mock_http_basic_cls: HTTPBasic,
    ):
        mock_http_basic_cls.return_value = mock.AsyncMock(spec=HTTPBasic, realm=None)
        mock_request = mock.MagicMock(spec=Request)
        basic_obj = mock_http_basic_cls()
        basic_obj.return_value = None
        doc_security = ApiDocSecurity(basic=basic_obj)

        with mock.patch("app.api.api_v1.auth.get_settings") as mock_get_settings:
            mock_get_settings.return_value = mock.Mock(
                ENV_NAME="prd",
                API_DOC_ENABLED=True,
                API_DOC_USER="my_user",
                API_DOC_PASSWORD=SecretStr("pass123"),
            )
            with pytest.raises(HTTPException) as exception:
                _ = await doc_security(mock_request)

            assert exception.value.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "user_name,user_pwd",
        [
            ("dummy1", "dummy2"),
            ("my_user", "dummy3"),
            ("dummy4", "password123"),
        ],
    )
    async def test_api_doc_enabled__prd_env_invalid_credentials(
        self,
        mock_http_basic_cls: HTTPBasic,
        user_name: str,
        user_pwd: str,
    ):
        mock_http_basic_cls.return_value = mock.AsyncMock(spec=HTTPBasic, realm=None)
        mock_request = mock.MagicMock(spec=Request)
        basic_obj = mock_http_basic_cls()
        basic_obj.return_value = HTTPBasicCredentials(
            username=user_name, password=user_pwd
        )
        doc_security = ApiDocSecurity(basic=basic_obj)

        with mock.patch("app.api.api_v1.auth.get_settings") as mock_get_settings:
            mock_get_settings.return_value = mock.Mock(
                ENV_NAME="prd",
                API_DOC_ENABLED=True,
                API_DOC_USER="my_user",
                API_DOC_PASSWORD=SecretStr("pass123"),
            )
            with pytest.raises(HTTPException) as exception:
                _ = await doc_security(mock_request)

            assert exception.value.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_api_doc_enabled__prd_env_valid_credentials(
        self,
        mock_http_basic_cls: HTTPBasic,
    ):
        mock_http_basic_cls.return_value = mock.AsyncMock(spec=HTTPBasic, realm=None)
        mock_request = mock.MagicMock(spec=Request)
        basic_obj = mock_http_basic_cls()
        expected_user_name = "my_user"
        expected_user_pwd = "pass123"
        basic_obj.return_value = HTTPBasicCredentials(
            username=expected_user_name, password=expected_user_pwd
        )
        doc_security = ApiDocSecurity(basic=basic_obj)

        with mock.patch("app.api.api_v1.auth.get_settings") as mock_get_settings:
            mock_get_settings.return_value = mock.Mock(
                ENV_NAME="prd",
                API_DOC_ENABLED=True,
                API_DOC_USER=expected_user_name,
                API_DOC_PASSWORD=SecretStr(expected_user_pwd),
            )
            user_name = await doc_security(mock_request)

        assert user_name == expected_user_name
