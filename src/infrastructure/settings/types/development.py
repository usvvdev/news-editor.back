# coding utf-8

import logging

from ....domain.core.settings import AppSettings
from ....domain.core.types import OpenAPISettings


class DevAppSettings(AppSettings):
    openapi_settings: OpenAPISettings = OpenAPISettings(
        debug=True,
        title="Dev News Application",
    )

    logging_level: int = logging.DEBUG
