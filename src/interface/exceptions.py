# coding utf-8

from fastapi import HTTPException


class InvalidError(HTTPException):
    def __init__(self, status_code: int, detail: str, *args, **kwargs) -> None:
        super().__init__(status_code=status_code, detail=detail)


class InvalidAccessToken(InvalidError):
    def __init__(
        self,
        detail: str = "Invalid access token provided",
        headers: dict = {"WWW-Authenticate": "Bearer"},
    ) -> None:
        super().__init__(status_code=401, detail=detail, headers=headers)


class InvalidRefreshToken(InvalidError):
    def __init__(
        self,
        detail: str = "Invalid refresh token provided",
        headers: dict = {"WWW-Authenticate": "Bearer"},
    ) -> None:
        super().__init__(status_code=401, detail=detail, headers=headers)


class InvalidCredentials(InvalidError):
    def __init__(
        self,
        detail: str = "Invalid credentials provided",
    ) -> None:
        super().__init__(status_code=401, detail=detail)
