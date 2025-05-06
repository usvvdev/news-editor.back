# coding utf-8

from .news import news_router

from .user import user_router

__all__: list[str] = [
    "news_router",
    "user_router",
]
