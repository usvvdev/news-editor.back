# coding utf-8

from functools import lru_cache

from typing import (
    Generator,
    TypeVar,
    Type,
    Any,
)

from ...domain.core.types import AppEnvTypes

from ...domain.core.settings import BaseAppSettings

from .types import (
    DevAppSettings,
    ProdAppSettings,
    TestAppSettings,
)


Settings = TypeVar(
    "Settings",
    DevAppSettings,
    ProdAppSettings,
    TestAppSettings,
)


class AppSettings:
    def __init__(
        self,
        env: AppEnvTypes = BaseAppSettings().app_env,
    ) -> None:
        self._env = env

    @lru_cache
    def __call__(
        self,
    ) -> Type[Settings]:
        if not hasattr(self, self._env):
            raise ValueError(f"Invalid environment: {self._env}")
        return next(
            getattr(self, self._env),
        )

    @property
    def dev(
        self,
    ) -> Generator[Type[Settings], Any, None]:
        yield DevAppSettings()

    @property
    def prod(
        self,
    ) -> Generator[Type[Settings], Any, None]:
        yield ProdAppSettings()

    @property
    def test(
        self,
    ) -> Generator[Type[Settings], Any, None]:
        yield TestAppSettings()


get_app_settings = AppSettings()
