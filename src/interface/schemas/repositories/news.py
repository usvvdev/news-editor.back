# coding utf-8

from typing import Annotated

from pendulum import DateTime, now

from datetime import date

from pydantic import Field, field_validator

from sqlalchemy import Select, desc

from ....domain.core.types import (
    Base,
    BaseFilter,
    PhotoSource,
)

from ....infrastructure.orm.db.models import APINews


class BaseNewsSchema(Base):
    title: Annotated[
        str,
        Field(...),
    ]
    image: Annotated[
        str | PhotoSource,
        Field(default="https://i.imgur.com/WBehwoc.jpeg"),
    ]
    content: Annotated[
        str,
        Field(...),
    ]
    datetime: Annotated[
        date,
        Field(default_factory=lambda: now().date()),
    ]
    is_published: Annotated[
        bool,
        Field(default=False),
    ]

    @field_validator("image", mode="after")
    @classmethod
    def set_image(
        cls,
        value: str | PhotoSource,
    ) -> str:
        if not isinstance(value, str):
            return value.src
        return value

    @field_validator("datetime", mode="after")
    @classmethod
    def format_created_at(
        cls,
        value: DateTime,
    ) -> str:
        return value.strftime("%d.%m.%Y")


class NewsFilter(BaseFilter):
    __model__: BaseNewsSchema = APINews

    is_published: Annotated[
        bool | None,
        Field(default=None),
    ]
    datetime__gte: Annotated[
        str | None,
        Field(default=None, alias="from_date"),
    ]
    datetime__lte: Annotated[
        str | None,
        Field(default=None, alias="to_date"),
    ]

    @field_validator("datetime__gte", "datetime__lte", mode="after")
    @classmethod
    def validate_date(
        cls,
        value: str | None,
    ) -> DateTime | None:
        if value is not None:
            return DateTime.strptime(value, "%d.%m.%Y").date()
        return value

    def filter(
        self,
        stmt: Select,
    ) -> Select:
        return super().filter(
            stmt.order_by(desc(self.__model__.datetime)),
        )


class PostNewsSchema(BaseNewsSchema):
    is_published: Annotated[
        int,
        Field(default=True),
    ]


class GetNewsSchema(BaseNewsSchema):
    id: Annotated[
        int,
        Field(...),
    ]
