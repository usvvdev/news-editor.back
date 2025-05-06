# ocding utf-8

from .news import NewsService

from .user import UserAuthService

__all__: list[str] = [
    "NewsService",
    "UserAuthService",
]
