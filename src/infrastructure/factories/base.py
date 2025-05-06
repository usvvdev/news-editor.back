# coding utf-8

from fastapi import Depends

from ...domain.core.settings import AppSettings
from ..settings import get_app_settings

from ...domain.core.tools import JWTAuthefication


class JWTAuthFactory:
    @staticmethod
    def get(
        settings: AppSettings = Depends(get_app_settings),
    ) -> JWTAuthefication:
        return JWTAuthefication(settings)
