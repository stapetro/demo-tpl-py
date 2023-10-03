"""
Unit test the config module.
"""
# pylint: disable=missing-class-docstring,missing-function-docstring,no-self-use,
import typing as t

import pytest
from pydantic import AnyHttpUrl, ValidationError

from app.core.config import Settings, get_settings


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
