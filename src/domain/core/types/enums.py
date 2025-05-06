# coding utf-8

from enum import Enum


class AppEnvTypes(str, Enum):
    prod: str = "prod"
    dev: str = "dev"
    test: str = "test"


class TokenTypes(str, Enum):
    access: str = "access"
    refresh: str = "refresh"


class TokenExpiries(int, Enum):
    access: int = 3600
    refresh: int = 86400
