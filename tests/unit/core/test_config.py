"""
Unit test the config module.
"""
import json
import logging

# pylint: disable=missing-class-docstring,missing-function-docstring,no-self-use,
import typing as t

import pytest
import uvicorn
from pydantic import AnyHttpUrl, ValidationError

from app.core.config import (
    AccessEcsLogFormatter,
    LoggerFactory,
    LoggingConfig,
    Settings,
    SomeCtx,
    get_settings,
)


@pytest.mark.unit
class TestSettings:
    @pytest.mark.parametrize(
        "config_key, config_value, value_type",
        [
            (
                "API_V1_STR",
                "/api/vDummy",
                str,
            ),
            (
                "PROJECT_NAME",
                "pytest_dummy_project",
                str,
            ),
            (
                "PYDEVD",
                "True",
                bool,
            ),
            (
                "PYDEVD_PORT",
                "12345",
                int,
            ),
            (
                "PYDEVD_HOST",
                "magicHost",
                str,
            ),
            (
                "ENV_NAME",
                "loc-unit-test",
                str,
            ),
        ],
    )
    def test_env_var_injection(self, monkeypatch, config_key, config_value, value_type):
        monkeypatch.setenv(config_key, config_value)

        settings = Settings()

        assert getattr(settings, config_key) == value_type(config_value)

    def test_backend_cors__values(self, monkeypatch):
        url_1 = "http://localhost"
        url_2 = "http://localhost:4200"
        url_3 = "http://localhost:3000"
        monkeypatch.setenv("BACKEND_CORS_ORIGINS", f'["{url_1}","{url_2}","{url_3}"]')

        settings = Settings()
        cors: t.List[AnyHttpUrl] = settings.BACKEND_CORS_ORIGINS

        assert cors[0] == AnyHttpUrl(url_1)
        assert cors[1] == AnyHttpUrl(url_2)
        assert cors[2] == AnyHttpUrl(url_3)

    def test_backend_cors__single_value(self, monkeypatch):
        url_1 = "http://localhost"
        monkeypatch.setenv("BACKEND_CORS_ORIGINS", f'"{url_1}"')

        settings = Settings()
        cors: t.List[AnyHttpUrl] = settings.BACKEND_CORS_ORIGINS

        assert cors[0] == AnyHttpUrl(url_1)

    def test_project_name__single_value(self, monkeypatch):
        expected_project_name = "cool project name"
        monkeypatch.setenv("PROJECT_NAME", expected_project_name)

        settings = Settings()

        assert settings.PROJECT_NAME == expected_project_name

    @pytest.mark.parametrize("config_key", ["BACKEND_CORS_ORIGINS"])
    @pytest.mark.parametrize(
        "invalid_url", ["brokenUrl", "brokenUrl:12345", "[]", "12345"]
    )
    def test_backend_cors__invalid_value(self, monkeypatch, config_key, invalid_url):
        monkeypatch.setenv(config_key, f'"{invalid_url}"')

        with pytest.raises(ValidationError):
            _ = Settings()

    @pytest.mark.parametrize(
        "config_key,config_value,version",
        [
            # GfK (or at least DIQC) convention: the app version is in
            # $VERSION. in every component / container, for every app.
            ("VERSION", "x.z.y", "x.z.y"),
            ("VERSION", "9.1.0", "9.1.0"),
            ("VERSION", "9.1.1", "9.1.1"),
            (" ", " ", "0.1.0"),
        ],
        ids=["Version x.z.y", "Version 9.1.0", "Version 9.1.1", "Default field value"],
    )
    def test_settings__version(self, monkeypatch, config_key, config_value, version):
        monkeypatch.setenv(config_key, config_value)
        settings = Settings()
        assert settings.VERSION == version

    def test_get_settings__cache(self):
        settings_1 = get_settings()
        settings_2 = get_settings()

        assert settings_1 is not None
        assert settings_2 is not None
        assert settings_1 is settings_2


@pytest.mark.unit
class TestLoggingConfig:
    def test_get_config__loc_env(self):
        env_name = "loc"
        log_config = LoggingConfig.get_config(env_name)

        assert log_config is uvicorn.config.LOGGING_CONFIG

    def test_get_config__central_env(self):
        env_name = "dev"
        log_config = LoggingConfig.get_config(env_name)

        assert log_config is not None
        assert log_config is LoggingConfig.ECS_UVICORN_LOGGING_CONFIG

    @pytest.mark.parametrize(
        "extra_fields",
        [None, {"user.email": "dummy@email.org"}],
        ids=["No extra fields", "With extra fields"],
    )
    def test_access_log_ecs_formatter__ok(self, extra_fields: dict[str, t.Any] | None):
        expected_lvl_name = "INFO"
        expected_client_address = "127.0.0.1:63075"
        expected_http_request_method = "GET"
        expected_url_path = "/api/v1/ping"
        expected_http_version = "1.1"
        expected_http_response_status_code = 200
        record = logging.makeLogRecord(
            {
                "args": (
                    expected_client_address,
                    expected_http_request_method,
                    expected_url_path,
                    expected_http_version,
                    expected_http_response_status_code,
                ),
                "created": 1692876214.468824,
                "filename": "h11_impl.py",
                "funcName": "send",
                "levelname": expected_lvl_name,
                "levelno": logging.INFO,
                "lineno": 478,
                "module": "h11_impl",
                "msecs": 468.0,
                "msg": '%s - "%s %s HTTP/%s" %d',
                "name": "uvicorn.access",
                "pathname": "Lib/site-packages/uvicorn/protocols/http/h11_impl.py",
                "process": 19340,
                "processName": "MainProcess",
                "relativeCreated": 1593974.9538898468,
                "thread": 29056,
                "threadName": "MainThread",
            }
        )

        formatter = AccessEcsLogFormatter(
            extra=extra_fields,
        )
        output_json_txt = formatter.format(record)
        output_dict = json.loads(output_json_txt)

        assert output_dict["log.level"] == str.lower(expected_lvl_name)
        assert output_dict["client"]["address"] == expected_client_address
        assert output_dict["http"]["request"]["method"] == expected_http_request_method
        assert output_dict["url"]["path"] == expected_url_path
        assert output_dict["http"]["version"] == expected_http_version
        assert (
            output_dict["http"]["response"]["status_code"]
            == expected_http_response_status_code
        )
        if extra_fields is not None:
            assert output_dict["user"]["email"] == extra_fields["user.email"]


@pytest.mark.unit
class TestLoggerFactory:
    def test_get_logger__no_context(self, caplog):
        expected_msg = "Dummy message"

        logger = LoggerFactory.get_logger("dummy_no_context")
        logger.warning(expected_msg)

        assert len(caplog.messages) == 1
        assert caplog.messages[0] == expected_msg
        assert len(caplog.records) == 1
        actual_record = caplog.records[0]
        assert actual_record.labels == {}

    def test_get_logger__with_context(self, caplog):
        mdc = SomeCtx(**{"userId": "abc123", "geoId": "def456"})
        expected_msg = "Dummy message"

        logger = LoggerFactory.get_logger("dummy_context", mdc)
        logger.warning(expected_msg)

        assert len(caplog.messages) == 1
        assert caplog.messages[0] == expected_msg
        assert len(caplog.records) == 1
        actual_record = caplog.records[0]
        assert actual_record.labels is not None
        self._compare_labels_with_ctx(actual_record.labels, mdc)

    @pytest.mark.parametrize(
        "initial_logger",
        [
            logging.getLogger("dummy_context_1"),
            LoggerFactory.get_logger("dummy_context_2"),
        ],
        ids=["Initial logger object", "Initial logger adapter object"],
    )
    def test_wrap_logger_with_ctx__ctx(self, caplog, initial_logger: logging.Logger):
        mdc = SomeCtx(**{"userId": "def456", "geoId": "abc123"})
        expected_msg_1 = "Dummy message 1"
        expected_msg_2 = "Dummy message 2"

        initial_logger.warning(expected_msg_1)
        logger_with_ctx = LoggerFactory.wrap_logger_with_ctx(initial_logger, mdc)
        logger_with_ctx.warning(expected_msg_2)

        assert len(caplog.messages) == 2
        assert len(caplog.records) == 2
        assert caplog.messages[0] == expected_msg_1
        actual_record_1 = caplog.records[0]
        if isinstance(initial_logger, logging.LoggerAdapter):
            assert len(actual_record_1.labels) == 0
        else:
            with pytest.raises(AttributeError):
                _ = actual_record_1.labels
        assert caplog.messages[1] == expected_msg_2
        actual_record_2 = caplog.records[1]
        assert actual_record_2.labels is not None
        self._compare_labels_with_ctx(actual_record_2.labels, mdc)

    @classmethod
    def _compare_labels_with_ctx(cls, record_labels: dict[str, t.Any], mdc: SomeCtx):
        assert record_labels["userId"] == mdc.userId
        assert record_labels["geoId"] == mdc.geoId
