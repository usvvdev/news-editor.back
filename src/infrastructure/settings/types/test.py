# coding utf-8

import logging

from ....domain.core.settings import AppSettings
from ....domain.core.types import OpenAPISettings


class TestAppSettings(AppSettings):
    openapi_settings: OpenAPISettings = OpenAPISettings(
        debug=True,
        title="Test News Application",
    )

    pool_size: int = 5

    logging_level: int = logging.DEBUG
