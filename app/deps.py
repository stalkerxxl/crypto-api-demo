from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from db import db_session
from db.crud import get_user_by_email
from exceptions import AuthError
from models import User
from services.auth import get_email_from_token

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/users/login", scheme_name="JWT")


def get_db():
    db: Session = db_session()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_schema)
):
    email: str = get_email_from_token(token)
    user = get_user_by_email(db, email)
    if user is None:
        raise AuthError(detail="Could not validate credentials")
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_banned:
        raise AuthError(status_code=400, detail="Inactive user")
    return current_user


def get_current_admin_user(current_user: User = Depends(get_current_active_user)):
    if not current_user.is_admin:
        raise AuthError(status_code=400, detail="You are not admin")
    return current_user
