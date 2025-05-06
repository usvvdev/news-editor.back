# coding utf-8

from ..core import Database, BaseRepository

from ..models import AuthUser


class AuthUserRepository(BaseRepository):
    def __init__(
        self,
        database: Database,
    ) -> None:
        super().__init__(
            database,
            AuthUser,
        )

    async def get_user_by_username(
        self,
        username: str,
    ) -> AuthUser | None:
        return await self.get_by_field_name(
            "username",
            username,
        )

    async def get_user_by_uuid(
        self,
        uuid: str,
    ) -> AuthUser | None:
        return await self.get_by_field_name(
            "uuid",
            uuid,
        )
