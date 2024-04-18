from fastapi import Depends, Response, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.crud import user_exists, create_user, delete_user
from deps import (
    get_current_user,
    get_db,
    get_current_active_user,
    get_current_admin_user,
)
from exceptions import AuthError
from models import User
from schemas.token import TokenType, TokenOut
from schemas.user import UserCreate, UserOut
from services.auth import (
    create_token_by_type,
    create_both_tokens,
    authenticate_user,
    encode_password,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=TokenOut)
async def register(
    response: Response, user_form: UserCreate, db: Session = Depends(get_db)
):
    if user_exists(db, user_form.email):
        raise AuthError(status_code=400, detail="User with this email already exists")
    user_form.password = encode_password(user_form.password)
    user = create_user(db, user_form)
    access_token, refresh_token = create_both_tokens(data={"sub": user.email})
    await _set_refresh_token(response, refresh_token)
    return TokenOut(access_token=access_token)


@router.post("/login", response_model=TokenOut)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user: User = authenticate_user(db, form_data.username, form_data.password)
    access_token, refresh_token = create_both_tokens(data={"sub": user.email})
    await _set_refresh_token(response, refresh_token)
    return TokenOut(access_token=access_token)


@router.post("/refresh-token", response_model=TokenOut)
async def refresh_access_token(user: User = Depends(get_current_user)):
    access_token = create_token_by_type(
        data={"sub": user.email}, token_type=TokenType.ACCESS
    )
    return TokenOut(access_token=access_token)


@router.get("/profile", response_model=UserOut)
async def read_profile(current_user: User = Depends(get_current_active_user)):
    return UserOut.model_validate(current_user)


@router.delete("/delete/{user_id}", dependencies=[Depends(get_current_admin_user)])
async def delete(user_id: int, db: Session = Depends(get_db)):
    result = delete_user(db, user_id)
    if not bool(result):
        raise AuthError(status_code=404, detail="User not found and not deleted")
    return {"User deleted successfully"}


async def _set_refresh_token(response: Response, refresh_token):
    response.set_cookie("refresh_token", refresh_token, httponly=True)
