# coding utf-8

from jwt import encode, decode

from typing import (
    List,
    Dict,
    Any,
    Type,
    TypeVar,
    Generator,
    Mapping,
)

from ..settings import AppSettings

from ..types import (
    RefreshTokenSchema,
    AccessTokenSchema,
    AuthUserSchema,
    BaseTokenSchema,
)

from jwt import (
    InvalidAlgorithmError,
    InvalidSignatureError,
    InvalidTokenError,
)

from ....interface.exceptions import InvalidRefreshToken


AccessToken = TypeVar(
    "AccessToken",
    bound=[AccessTokenSchema],
)

UserTokens = TypeVar(
    "UserTokens",
    RefreshTokenSchema,
    AccessTokenSchema,
)

RefreshError = TypeVar(
    "RefreshError",
    InvalidAlgorithmError,
    InvalidSignatureError,
    InvalidTokenError,
)


class JWTAuthefication:
    def __init__(
        self,
        settings: AppSettings,
    ) -> None:
        self._settings = settings

    def encode_token(
        self,
        token: Type[UserTokens],
    ) -> str:
        return encode(
            token.model_dump(
                by_alias=True,
                exclude_none=True,
            ),
            key=self._settings.secret_key,
            algorithm=self._settings.algorithm,
        )

    def decode_token(
        self,
        token: str,
    ) -> BaseTokenSchema:
        try:
            data: Dict[str, Any] = decode(
                token,
                key=self._settings.secret_key,
                algorithms=[
                    self._settings.algorithm,
                ],
            )
        except RefreshError:
            raise InvalidRefreshToken
        return BaseTokenSchema(**data)

    def __call__(
        self,
        user_data: Dict[str, Any],
        schemas: List[UserTokens],
    ) -> AuthUserSchema:
        token_data: Mapping[UserTokens, Any] = next(
            self.generate_token(user_data, schemas),
        )
        return AuthUserSchema(**dict(token_data))

    def generate_token(
        self,
        user_data: Dict[str, Any],
        token_schemas: List[UserTokens],
    ) -> Generator[Mapping[UserTokens, Any], Any, None]:
        yield map(
            lambda token: (
                token.model_config.get("title"),
                self.encode_token(
                    token(**user_data),
                ),
            ),
            token_schemas,
        )
