# coding utf-8

from typing import AsyncGenerator, Any

from re import sub

from sqlalchemy.orm import sessionmaker, class_mapper

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from ...domain.core.settings import AppSettings


@as_declarative()
class BaseModel:
    __name__: str

    @declared_attr
    def __tablename__(
        cls,
    ) -> str:
        return sub(
            r"(?<!^)([A-Z][a-z])",
            r"_\1",
            cls.__name__,
        ).lower()

    @property
    def to_dict(
        self,
    ) -> dict[str, Any]:
        return dict(
            (
                column.key,
                getattr(self, column.key),
            )
            for column in class_mapper(self.__class__).columns
        )


class BaseDatabaseEngine:
    def __init__(
        self,
        settings: AppSettings,
        engine_url: str,
    ) -> None:
        self._engine: AsyncEngine = create_async_engine(
            str(engine_url),
            future=True,
            echo=settings.openapi_settings.debug,
        )
        self._session_factory = sessionmaker(
            self._engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def set_session(
        self,
    ) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_factory() as session:
            yield session
