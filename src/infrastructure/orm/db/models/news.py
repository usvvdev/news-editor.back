# coding utf-8

from sqlalchemy import (
    Column,
    String,
    Integer,
    Identity,
    Date,
)
from sqlalchemy.dialects.mysql import LONGTEXT, TINYINT

from datetime import date

from ...base import BaseModel


class APINews(BaseModel):
    id: int = Column(
        Integer,
        Identity(),
        primary_key=True,
        index=True,
    )
    datetime: date = Column(
        Date,
        nullable=False,
    )
    title: str = Column(
        String(length=128),
        nullable=False,
    )
    content: str = Column(
        LONGTEXT,
        nullable=False,
    )
    image: str = Column(
        LONGTEXT,
        nullable=False,
    )
    is_published: int = Column(
        TINYINT(1),
        default=0,
        nullable=False,
    )
