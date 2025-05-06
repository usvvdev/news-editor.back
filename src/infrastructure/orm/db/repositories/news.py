# coding utf-8

from typing import Any, Sequence

from sqlalchemy import (
    CursorResult,
    Result,
    update,
    insert,
    select,
)

from ..core import Database, BaseRepository, Base
from ..models import APINews

from .....interface.schemas.repositories import (
    PostNewsSchema,
    NewsFilter,
)


class NewsRepositry(BaseRepository):
    def __init__(
        self,
        database: Database,
    ) -> None:
        super().__init__(database, APINews)

    async def get_all_news(
        self,
        filters: NewsFilter,
    ) -> Sequence | None:
        async for session in self._database.set_session():
            result: Result[tuple[Base]] = await session.execute(
                filters.filter(
                    select(self._model),
                ),
            )
            return result.scalars().all()

    async def get_news_by_id(
        self,
        id: int,
    ) -> APINews | None:
        return self.get_by_field_name(
            "id",
            id,
        )

    async def add_news_item(
        self,
        data: PostNewsSchema,
    ) -> None:
        async for session in self._database.set_session():
            _: CursorResult[Any] = await session.execute(
                insert(self._model).values(
                    **data.dict,
                ),
            )
            return await session.commit()

    async def update_news_by_id(
        self,
        id: int,
        data: PostNewsSchema,
    ) -> None:
        async for session in self._database.set_session():
            _: CursorResult[Any] = await session.execute(
                update(self._model)
                .where(self._model.id == id)
                .values(
                    **data.dict,
                )
            )
            return await session.commit()
