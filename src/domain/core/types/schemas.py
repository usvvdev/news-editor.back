# coding utf-8

from typing import Annotated, Type, Any

from pathlib import Path

from io import BytesIO
from PIL.Image import Image, open
from base64 import decodebytes

from pendulum import now

from uuid import uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)

from sqlalchemy.ext.declarative import DeclarativeMeta

from fastapi_filter.contrib.sqlalchemy import Filter

from .enums import TokenTypes, TokenExpiries


class Base(BaseModel):
    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        validate_default=True,
        use_enum_values=True,
        populate_by_name=True,
    )

    @property
    def dict(
        self,
    ) -> dict[str, Any]:
        return self.model_dump()


class BaseFilter(Filter):
    __model__: Type[DeclarativeMeta]

    def __init_subclass__(
        cls,
        **kwargs: ConfigDict,
    ) -> None:
        super().__init_subclass__(**kwargs)
        cls.Constants.model = cls.__model__

    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        validate_default=True,
        populate_by_name=True,
        extra="allow",
    )


class OpenAPISettings(Base):
    debug: Annotated[
        bool,
        Field(default=False),
    ]
    docs_url: Annotated[
        str,
        Field(default="/docs"),
    ]
    openapi_prefix: Annotated[
        str,
        Field(default=""),
    ]
    openapi_url: Annotated[
        str,
        Field(default="/openapi.json"),
    ]
    redoc_url: Annotated[
        str,
        Field(default="/redoc"),
    ]
    title: Annotated[
        str,
        Field(default="News Application"),
    ]
    version: Annotated[
        str,
        Field(default="0.1.0"),
    ]


class SuccessMessage(Base):
    message: Annotated[
        str,
        Field(default="OK"),
    ]


class PhotoSource(BaseModel):
    media_path: Annotated[
        str,
        Field(default="media/", exclude=True),
    ]
    name: Annotated[
        str,
        Field(...),
    ]
    src: Annotated[
        Any,
        Field(...),
    ]

    @field_validator("src", mode="before")
    @classmethod
    def save_media_source(
        cls,
        value: str,
        values: dict[str, Any],
    ) -> None:
        img: Image = open(
            BytesIO(
                decodebytes(
                    cls.split_src_value(
                        value,
                        ",",
                    ).encode("utf-8")
                )
            )
        )
        return img.save(cls.source_path(values))

    @field_validator("src", mode="after")
    @classmethod
    def set_media_source_path(
        cls,
        _: str,
        values: dict[str, Any],
    ) -> str:
        return cls.source_path(values)

    @classmethod
    def source_path(
        cls,
        values: dict[str, Any],
    ) -> str:
        data: dict[str, Any] = values.data
        return str(
            Path(data.get("media_path")) / f"{data['name']}",
        )

    @classmethod
    def split_src_value(
        cls,
        value: str,
        separator: str,
    ) -> str:
        return value.split(separator)[-1]


class BaseTokenSchema(Base):
    typ: Annotated[
        TokenTypes,
        Field(...),
    ]
    uuid: Annotated[
        str,
        Field(..., alias="sub"),
    ]
    exp: Annotated[
        int,
        Field(...),
    ]
    iat: Annotated[
        int,
        Field(
            default_factory=lambda: int(now().timestamp()),
        ),
    ]
    jti: Annotated[
        str,
        Field(
            default_factory=lambda: str(uuid4()),
        ),
    ]


class AccessTokenSchema(BaseTokenSchema, title="access_token"):
    typ: Annotated[
        TokenTypes,
        Field(
            default=TokenTypes.access,
        ),
    ]

    exp: Annotated[
        int,
        Field(
            default_factory=lambda: int(
                now()
                .add(
                    seconds=TokenExpiries.access,
                )
                .timestamp(),
            )
        ),
    ]


class RefreshTokenSchema(BaseTokenSchema, title="refresh_token"):
    typ: Annotated[
        TokenTypes,
        Field(
            default=TokenTypes.refresh,
        ),
    ]

    exp: Annotated[
        int,
        Field(
            default_factory=lambda: int(
                now()
                .add(
                    seconds=TokenExpiries.refresh,
                )
                .timestamp(),
            )
        ),
    ]


class AuthUserSchema(Base):
    token_type: Annotated[
        str,
        Field(
            default="Bearer",
        ),
    ]
    access_token: Annotated[
        str,
        Field(...),
    ]
    refresh_token: Annotated[
        str | None,
        Field(
            default=None,
        ),
    ]
