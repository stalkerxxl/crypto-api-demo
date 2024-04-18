from datetime import timedelta, datetime

import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import JWT_SECRET_KEY, JWT_ACCESS_TIME, JWT_REFRESH_TIME, JWT_ALGORITHM
from db.crud import get_user_by_email
from exceptions import AuthError
from models import User
from schemas.token import TokenType

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_email_from_token(token: str) -> str:
    err_msg = "Could not validate credentials"
    try:
        payload = decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise AuthError(detail=err_msg)
    except jwt.InvalidTokenError:
        raise AuthError(detail=err_msg)
    return email


def create_token_by_type(data: dict, token_type: TokenType) -> str:
    to_encode = data.copy()
    if token_type == TokenType.ACCESS:
        expires_delta = timedelta(minutes=JWT_ACCESS_TIME)
    else:
        expires_delta = timedelta(minutes=JWT_REFRESH_TIME)
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def create_both_tokens(data: dict) -> tuple[str, str]:
    access_token = create_token_by_type(data=data, token_type=TokenType.ACCESS)
    refresh_token = create_token_by_type(data=data, token_type=TokenType.REFRESH)
    return access_token, refresh_token


def authenticate_user(db: Session, email: str, password: str) -> User:
    err_msg = "Incorrect username or password"
    user: User | None = get_user_by_email(db, email)
    if not user:
        raise AuthError(detail=err_msg)
    elif not verify_password(password, user.hashed_password):
        raise AuthError(detail=err_msg)
    return user


def decode_token(token: str):
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def encode_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def decode_password(hashed_password: str):
    pass
