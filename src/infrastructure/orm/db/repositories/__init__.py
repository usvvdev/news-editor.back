# coding utf-8

from .news import NewsRepositry
from .user import AuthUserRepository

__all__: list[str] = [
    "NewsRepositry",
    "AuthUserRepository",
]
