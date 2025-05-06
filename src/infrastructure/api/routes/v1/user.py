# coding utf-8

from fastapi import APIRouter, Depends

from ...views.v1 import AuthUserView
from ....factories.resources import AuthUserViewFactory

from .....interface.schemas.repositories import UserAuthSchema, UserRefreshSchema

from .....domain.core.tools import auto_docs
from .....domain.core.types import AuthUserSchema


user_router = APIRouter(prefix="/auth", tags=["User Auth"])


@user_router.post(
    "/token",
    response_model=AuthUserSchema,
)
@auto_docs(
    user_router.prefix,
    "POST",
    description="Performs user authentication using the specified **parameters**.",
    params={
        "username": {
            "type": "string",
            "description": "Username of user.",
        },
        "password": {
            "type": "string",
            "description": "Password for user account.",
        },
    },
)
async def user_authorization(
    data: UserAuthSchema,
    view: AuthUserView = Depends(AuthUserViewFactory.create),
) -> AuthUserSchema:
    return await view.user_authorization(
        data,
    )


@user_router.post(
    "/refresh",
    response_model=AuthUserSchema,
    response_model_exclude_none=True,
    response_model_exclude="token_type",
)
@auto_docs(
    user_router.prefix,
    "POST",
    description="Getting new one authentication parameters for user.",
    params={
        "refresh_token": {
            "type": "string",
            "description": "Refresh token of the authorized user.",
        },
    },
)
async def generate_new_access_token(
    data: UserRefreshSchema,
    view: AuthUserView = Depends(AuthUserViewFactory.create),
) -> AuthUserSchema:
    return await view.generate_new_access_token(
        data,
    )
