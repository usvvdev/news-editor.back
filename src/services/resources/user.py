# coding utf-8

from ...domain.core.tools import (
    JWTAuthefication,
    UserTokens,
    AccessToken,
)

from ...infrastructure.orm.db.models import AuthUser

from ...infrastructure.orm.db.repositories import AuthUserRepository

from ...interface.schemas.repositories import (
    UserAuthSchema,
    UserRefreshSchema,
)
from ...domain.core.types import AuthUserSchema, BaseTokenSchema

from ...interface.exceptions import InvalidCredentials, InvalidRefreshToken


class UserAuthService:
    def __init__(
        self,
        repository: AuthUserRepository,
        auth: JWTAuthefication,
    ) -> None:
        self._repository = repository
        self._auth = auth

    async def generate_user_auth(
        self,
        data: UserAuthSchema,
    ) -> AuthUserSchema:
        user: AuthUser = await self._repository.get_user_by_username(
            data.username,
        )
        if not user or not data(user.password):
            raise InvalidCredentials
        return self._auth(user.to_dict, UserTokens.__constraints__)

    async def generate_new_access_token(
        self,
        data: UserRefreshSchema,
    ) -> AuthUserSchema:
        user: AuthUser = await self._repository.get_user_by_uuid(
            self._auth.decode_token(data.refresh_token).uuid,
        )
        if not user:
            raise InvalidRefreshToken
        return self._auth(user.to_dict, AccessToken.__bound__)
