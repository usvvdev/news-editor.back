# coding utf-8

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.domain.core.settings.app import AppSettings
from src.infrastructure.settings.core import get_app_settings

from src.infrastructure.server.tools import AppRouter


def main() -> FastAPI:
    settings: AppSettings = get_app_settings()

    app = FastAPI(**settings.app_settings)
    app_router = AppRouter(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
    )
    app_router()

    return app


if __name__ == "__main__":
    main()
