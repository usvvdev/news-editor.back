# coding utf-8

from .news import NewsView

from .user import AuthUserView

__all__: list[str] = [
    "NewsView",
    "AuthUserView",
]
