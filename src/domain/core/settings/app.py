# coding utf-8

import logging

from typing import (
    Any,
    List,
    Dict,
    Tuple,
    Annotated,
)

from pydantic import MySQLDsn, Field

from ..settings import BaseAppSettings

from ..types import OpenAPISettings


class AppSettings(BaseAppSettings):
    database_url: MySQLDsn
    pool_size: Annotated[
        int,
        Field(default=10),
    ]
    pre_ping: Annotated[
        bool,
        Field(default=True),
    ]

    algorithm: Annotated[
        str,
        Field(default=""),
    ]
    secret_key: Annotated[
        str,
        Field(default=""),
    ]

    decode_response: Annotated[
        bool,
        Field(default=True),
    ]

    api_prefix: Annotated[
        str,
        Field(default="/api"),
    ]
    allowed_hosts: Annotated[
        List[str],
        Field(default=["*"]),
    ]

    logging_level: Annotated[
        int,
        Field(default=logging.INFO),
    ]
    loggers: Annotated[
        Tuple[str, ...],
        Field(default=("uvicorn.asgi", "uvicorn.access")),
    ]

    openapi_settings: Annotated[
        OpenAPISettings,
        Field(default=OpenAPISettings),
    ]

    @property
    def app_settings(
        self,
    ) -> Dict[str, Any]:
        return self.openapi_settings.dict
