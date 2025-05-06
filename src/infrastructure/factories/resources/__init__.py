# coding utf-8

from .news import NewsViewFactory

from .user import AuthUserViewFactory

__all__: list[str] = [
    "NewsViewFactory",
    "AuthUserViewFactory",
]
