from fastapi import HTTPException


class AuthError(HTTPException):
    def __init__(
        self,
        status_code: int = 401,
        detail: str = "Authorization failed",
        headers: dict[str, str] | None = None,
    ) -> None:
        if headers is None:
            headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(status_code=status_code, detail=detail, headers=headers)
