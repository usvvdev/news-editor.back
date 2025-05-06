# coding utf-8

from typing import List

from .....domain.core.types import SuccessMessage

from .....interface.schemas.repositories import (
    GetNewsSchema,
    PostNewsSchema,
    NewsFilter,
)
from .....services.resources import NewsService


class NewsView:
    def __init__(
        self,
        service: NewsService,
    ) -> None:
        self._service = service

    async def get_all_news(
        self,
        filters: NewsFilter,
    ) -> List[GetNewsSchema]:
        return await self._service.get_all_news(filters)

    async def get_news_by_id(
        self,
        id: int,
    ) -> GetNewsSchema:
        return await self._service.get_news_by_id(id)

    async def add_news_item(
        self,
        data: PostNewsSchema,
    ) -> GetNewsSchema:
        return await self._service.add_news_item(data)

    async def update_news_by_id(
        self,
        id: int,
        data: PostNewsSchema,
    ) -> SuccessMessage:
        return await self._service.update_news_by_id(id, data)
