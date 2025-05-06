# coding utf-8

from .....services.resources import UserAuthService

from .....domain.core.types import AuthUserSchema

from .....interface.schemas.repositories import UserAuthSchema, UserRefreshSchema


class AuthUserView:
    def __init__(
        self,
        service: UserAuthService,
    ) -> None:
        self._service = service

    async def user_authorization(
        self,
        data: UserAuthSchema,
    ) -> AuthUserSchema:
        return await self._service.generate_user_auth(
            data,
        )

    async def generate_new_access_token(
        self,
        data: UserRefreshSchema,
    ) -> AuthUserSchema:
        return await self._service.generate_new_access_token(
            data,
        )
