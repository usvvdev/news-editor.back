# coding utf-8

from os import getenv

from pydantic_settings import SettingsConfigDict, BaseSettings

from ..types import AppEnvTypes


class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = AppEnvTypes(getenv("APP_ENV", "dev"))

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env",
        extra="allow",
        validate_assignment=True,
    )
