# coding utf-8

from typing import Callable, Any

from fastapi import Depends

from fastapi.security import OAuth2PasswordBearer

from jwt import (
    decode,
    ExpiredSignatureError,
    DecodeError,
)

from ..settings import AppSettings
from ....infrastructure.settings import get_app_settings

from ....interface.exceptions import InvalidAccessToken


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/token",
)


def validate_token(
    settings: AppSettings = Depends(get_app_settings),
    token: str = Depends(oauth2_scheme),
) -> Any:
    try:
        payload = decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
    except (ExpiredSignatureError, DecodeError):
        raise InvalidAccessToken
    return payload


def auto_docs(
    path: str,
    method: str,
    description: str | None = None,
    params: dict[str, dict[str, str]] | None = None,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        param_docs = "\n".join(
            f"| {name} | {info['type']} | {info['description']} |"
            for name, info in (params or {}).items()
        )
        func.__doc__ = (
            f"- **{method.upper()} `{path}`**\n\n{description or ''}\n"
            f"### Parameters:\n\n"
            f"| Parameter | Type | Description |\n|-----------|------|-------------|\n{param_docs}"
        )
        return func

    return decorator
