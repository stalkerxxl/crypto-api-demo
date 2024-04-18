from enum import Enum

from pydantic import BaseModel, Field


class TokenOut(BaseModel):
    access_token: str | bytes
    token_type: str | None = Field(default="Bearer")


class TokenType(str, Enum):
    ACCESS = "ACCESS_TOKEN"
    REFRESH = "REFRESH_TOKEN"
