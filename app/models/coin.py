from datetime import datetime

from sqlalchemy import BigInteger, func
from sqlalchemy.orm import mapped_column, Mapped

from app.models.base import Base


class Coin(Base):
    __tablename__ = "coins"

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    open: Mapped[float] = mapped_column(nullable=False)
    close: Mapped[float]
    changes_percentage: Mapped[float]
    change: Mapped[float]
    day_low: Mapped[float]
    day_high: Mapped[float]
    year_low: Mapped[float]
    year_high: Mapped[float]
    market_cap: Mapped[float]
    avg_50: Mapped[float]
    avg_200: Mapped[float]
    volume: Mapped[float]
    avg_volume: Mapped[float]
    shares: Mapped[int]
    api_timestamp: Mapped[int] = mapped_column(BigInteger(), nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )
