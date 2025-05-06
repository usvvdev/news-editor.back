# coding utf-8

from fastapi import Depends

from ....domain.core.settings import AppSettings
from ...settings.core import get_app_settings

from ...orm.db.core import Database
from ...orm.db.repositories import AuthUserRepository

from ....services.resources import UserAuthService
from ...api.views.v1 import AuthUserView

from ....domain.core.tools import JWTAuthefication
from ..base import JWTAuthFactory


class AuthUserRepositoryFactory:
    @staticmethod
    def get(
        settings: AppSettings = Depends(get_app_settings),
    ) -> AuthUserRepository:
        return AuthUserRepository(Database(settings))


class AuthUserServiceFactory:
    @staticmethod
    def get(
        repository: AuthUserRepository = Depends(
            AuthUserRepositoryFactory.get,
        ),
        authorization: JWTAuthefication = Depends(
            JWTAuthFactory.get,
        ),
    ) -> UserAuthService:
        return UserAuthService(repository, authorization)


class AuthUserViewFactory:
    @staticmethod
    def create(
        service: UserAuthService = Depends(
            AuthUserServiceFactory.get,
        ),
    ) -> AuthUserView:
        return AuthUserView(service)
