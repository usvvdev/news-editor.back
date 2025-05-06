# coding utf-8

from typing import List

from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends

from ...views.v1 import NewsView
from ....factories.resources import NewsViewFactory

from .....domain.core.tools import auto_docs, validate_token
from .....domain.core.types import SuccessMessage, AuthUserSchema

from .....interface.schemas.repositories import (
    GetNewsSchema,
    PostNewsSchema,
    NewsFilter,
)


news_router = APIRouter(prefix="/news", tags=["News API"])


@news_router.get("", response_model=List[GetNewsSchema])
@auto_docs(
    news_router.prefix,
    "GET",
    description="Retrieves all available news for the specified **PERIOD**.",
    params={
        "is_publsied": {
            "type": "boolean",
            "description": "The status of the news publication",
        },
        "from_date": {
            "type": "string",
            "description": "The date from which the news search will be performed",
        },
        "to_date": {
            "type": "string",
            "description": "The date starting from which the news search will be performed",
        },
    },
)
async def get_news(
    filters: NewsFilter = FilterDepends(NewsFilter),
    view: NewsView = Depends(NewsViewFactory.create),
) -> List[GetNewsSchema]:
    return await view.get_all_news(filters)


@news_router.get("/{id}", response_model=GetNewsSchema)
@auto_docs(
    "".join((news_router.prefix, "{id}")),
    "GET",
    description="Retrieves the available news by the specified **ID**",
    params={
        "id": {
            "type": "integer",
            "description": "The identifier by which the news was published",
        }
    },
)
async def get_news_by_id(
    id: int,
    view: NewsView = Depends(NewsViewFactory.create),
) -> GetNewsSchema:
    return await view.get_news_by_id(id)


@news_router.post("", response_model=SuccessMessage)
@auto_docs(
    news_router.prefix,
    "POST",
    description="Add new news according to the specified parameters.",
    params={
        "title": {
            "type": "string",
            "description": "The title of the specifed news",
        },
        "content": {
            "type": "string",
            "description": "The description of the specifed news",
        },
    },
)
async def add_news_item(
    data: PostNewsSchema,
    view: NewsView = Depends(NewsViewFactory.create),
    _: AuthUserSchema = Depends(validate_token),
) -> SuccessMessage:
    return await view.add_news_item(data)


@news_router.put("/{id}", response_model=SuccessMessage)
@auto_docs(
    "".join((news_router.prefix, "{id}")),
    "PUT",
    description="Updates the specified available news set by **ID**.",
    params={
        "id": {
            "type": "integer",
            "description": "The identifier by which the news was published",
        },
        "content": {
            "type": "string",
            "description": "The description of the specifed news",
        },
        "is_published": {
            "type": "boolean",
            "description": "The status of the news publication",
        },
    },
)
async def update_news_by_id(
    data: PostNewsSchema,
    id: int,
    view: NewsView = Depends(NewsViewFactory.create),
    _: AuthUserSchema = Depends(validate_token),
) -> SuccessMessage:
    return await view.update_news_by_id(id, data)
