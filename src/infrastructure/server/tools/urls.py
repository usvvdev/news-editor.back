# coding utf-8

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from ..core import BaseAppRouter

from ...api.routes.v1 import news_router, user_router


class AppRouter(BaseAppRouter):
    def __init__(
        self,
        app: FastAPI,
        meida_path: str = "media",
    ) -> None:
        app.mount(
            "".join(("/", meida_path)),
            StaticFiles(directory=meida_path),
            name=meida_path,
        )
        super().__init__(
            app,
            routers=[news_router, user_router],
        )
