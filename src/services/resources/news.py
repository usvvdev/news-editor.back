# coding utf-8

from typing import List

from ...domain.core.types import SuccessMessage

from ...interface.schemas.repositories import (
    GetNewsSchema,
    PostNewsSchema,
    NewsFilter,
)
from ...infrastructure.orm.db.repositories import NewsRepositry


class NewsService:
    def __init__(
        self,
        repository: NewsRepositry,
    ) -> None:
        self._repositry = repository

    async def get_all_news(
        self,
        filters: NewsFilter,
    ) -> List[GetNewsSchema]:
        return await self._repositry.get_all_news(
            filters,
        )

    async def get_news_by_id(
        self,
        id: int,
    ) -> GetNewsSchema:
        return await self._repositry.get_news_by_id(
            id,
        )

    async def add_news_item(
        self,
        data: PostNewsSchema,
    ) -> SuccessMessage:
        _: None = await self._repositry.add_news_item(
            data,
        )
        return SuccessMessage

    async def update_news_by_id(
        self,
        id: int,
        data: PostNewsSchema,
    ) -> SuccessMessage:
        _: None = await self._repositry.update_news_by_id(
            id,
            data,
        )
        return SuccessMessage
