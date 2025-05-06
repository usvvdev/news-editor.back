# coding utf-8

from typing import Annotated

from pydantic import Field

from passlib.context import CryptContext

from ....domain.core.types import Base


pwd_context: CryptContext = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


class UserAuthSchema(Base):
    username: Annotated[
        str,
        Field(...),
    ]
    password: Annotated[
        str,
        Field(...),
    ]

    def __call__(
        self,
        hashed_password: str,
    ) -> bool:
        return pwd_context.verify(
            self.password,
            hashed_password,
        )


class UserRefreshSchema(Base):
    refresh_token: Annotated[
        str,
        Field(...),
    ]
