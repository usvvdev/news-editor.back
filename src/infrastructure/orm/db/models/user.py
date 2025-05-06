# coding utf-8

from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
)
from sqlalchemy.dialects.mysql import TINYINT

from ...base import BaseModel


class AuthUser(BaseModel):
    uuid: str = Column(
        String,
        default=uuid4(),
        nullable=False,
        primary_key=True,
    )
    username: str = Column(
        String(150),
        nullable=False,
        primary_key=True,
    )
    email: str = Column(
        String(254),
        nullable=False,
        primary_key=True,
    )
    is_active: int = Column(
        TINYINT(1),
        default=1,
        nullable=False,
    )
    password: str = Column(
        String(128),
        nullable=False,
    )
