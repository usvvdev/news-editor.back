# coding utf-8

from fastapi import FastAPI, APIRouter

from typing import (
    Generator,
    List,
    Any,
)

from ...domain.core.settings import AppSettings

from ..settings import get_app_settings


class BaseAppRouter:
    def __init__(
        self,
        app: FastAPI,
        routers: List[APIRouter],
        settings: AppSettings = get_app_settings(),
    ) -> None:
        self._app = app
        self._routers = routers
        self._settings = settings

    def __call__(
        self,
    ) -> List[APIRouter]:
        routers: map[APIRouter] = map(
            lambda router: next(
                self.__register_router(router),
            ),
            self._routers,
        )
        return list(routers)

    def __register_router(
        self,
        router: APIRouter,
    ) -> Generator[APIRouter, Any, None]:
        yield self._app.include_router(
            router,
            prefix=self._settings.api_prefix,
        )
