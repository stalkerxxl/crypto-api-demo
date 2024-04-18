from sqlalchemy.orm import Session

from models import User
from schemas.user import UserCreate, UserUpdate


def create_user(db: Session, user: UserCreate) -> User:
    user = User(**user.model_dump(by_alias=True))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: UserUpdate):
    pass


def delete_user(db: Session, user_id: int) -> int:
    result = db.query(User).filter(User.id == user_id).delete()
    db.commit()
    return result


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def user_exists(db: Session, email: str) -> bool:
    user = get_user_by_email(db, email)
    if user is not None:
        return True
    return False
