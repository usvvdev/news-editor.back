# coding utf-8

from typing import TypeVar, Any

from sqlalchemy import Result, select

from ..base import BaseDatabaseEngine, BaseModel
from ....domain.core.settings import AppSettings


Base = TypeVar("Base", bound=BaseModel)


class Database(BaseDatabaseEngine):
    def __init__(
        self,
        settings: AppSettings,
    ) -> None:
        super().__init__(
            settings,
            settings.database_url,
        )


class BaseRepository:
    def __init__(
        self,
        database: Database,
        model: type[Base],
    ) -> None:
        self._database = database
        self._model = model

    async def get_by_field_name(
        self,
        field: str,
        value: Any,
    ) -> Base | None:
        async for session in self._database.set_session():
            result: Result[Base] = await session.execute(
                select(self._model).where(
                    getattr(self._model, field) == value,
                )
            )
            return result.scalars().first()
