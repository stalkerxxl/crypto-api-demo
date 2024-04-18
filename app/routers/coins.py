from typing import List, Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_, desc
from sqlalchemy.orm import Session

from deps import get_db
from app.models import Coin
from app.schemas.coin import CoinOut
from app.schemas.enums import CoinFields, SortDirection

router = APIRouter(prefix="/coins", tags=["Coins"])
DEFAULT_LIMIT = 100


@router.get("/all", response_model=List[CoinOut])
async def all(limit: int = DEFAULT_LIMIT, skip: int = 0, session: Session = Depends(get_db)):
    data = session.query(Coin).offset(skip).limit(limit).all()
    return data


@router.get("/search", response_model=List[CoinOut])
async def search(query: Annotated[str, Query(min_length=2)], session: Session = Depends(get_db)):
    data = session.query(Coin).filter(
        or_(
            Coin.symbol.contains(query),
            Coin.name.contains(query)
        )
    ).all()
    return data


@router.get("/most-active", response_model=List[CoinOut])
def most_active(session: Session = Depends(get_db)):
    data = session.query(Coin).order_by(desc(Coin.avg_volume)).limit(DEFAULT_LIMIT).all()
    return data


@router.get("/most-gainers", response_model=List[CoinOut])
def most_gainers(session: Session = Depends(get_db)):
    data = session.query(Coin).order_by(desc(Coin.changes_percentage)).limit(DEFAULT_LIMIT).all()
    return data


@router.get("/most-losers", response_model=List[CoinOut])  # FIXME переделать на ""
def most_losers(session: Session = Depends(get_db)):
    data = session.query(Coin).order_by(Coin.changes_percentage).limit(DEFAULT_LIMIT).all()
    return data


# noinspection PyUnboundLocalVariable
@router.get("/filter", response_model=List[CoinOut])
async def filter_by(order_by: CoinFields, sort_by: SortDirection, limit: int = DEFAULT_LIMIT, skip: int = 0,
                    session: Session = Depends(get_db)):
    sort_field = getattr(Coin, order_by.value)
    if sort_by == SortDirection.ASC:
        data = session.query(Coin).order_by(sort_field).offset(skip).limit(limit).all()
    elif sort_by == SortDirection.DESC:
        data = session.query(Coin).order_by(desc(sort_field)).offset(skip).limit(limit).all()
    return data


@router.get("/{symbol}", response_model=CoinOut)
async def coin(symbol: str, session: Session = Depends(get_db)):
    data = session.query(Coin).filter(Coin.symbol == symbol).one()
    return data
