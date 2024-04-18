from datetime import datetime

from pydantic import BaseModel


class CoinOut(BaseModel):
    symbol: str
    name: str
    price: float
    open: float
    close: float | None
    changes_percentage: float | None
    change: float | None
    day_low: float | None
    day_high: float | None
    year_low: float | None
    year_high: float | None
    market_cap: float | None
    avg_50: float | None
    avg_200: float | None
    volume: float | None
    avg_volume: float | None
    shares: float | None
    updated_at: datetime

    class Config:
        from_attributes = True
