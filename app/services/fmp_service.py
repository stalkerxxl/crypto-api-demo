import re
from datetime import datetime, timedelta

import httpx
from pydantic import ValidationError, BaseModel, Field, field_validator

from app.db import db_session
from app.models import Coin
from app.services import utils, fmp_client

logger = utils.get_logger(__name__)


async def update_coins_from_api():
    async with httpx.AsyncClient() as client:
        json = await fmp_client.get_full_quotes_list(client)
    for coin in json:
        __update_coin(coin)


def __update_coin(data: dict):
    try:
        dto = CoinDTO.model_validate(data)
    except ValidationError as err:
        logger.debug("%s ValidationError: %s", data["symbol"], str(err))
        return

    with db_session() as session:
        dto_dict = dto.model_dump()
        coin = session.query(Coin).filter_by(symbol=dto.symbol).one_or_none()
        if coin is None:
            coin = Coin(**dto_dict)
            session.add(coin)
        else:
            for k, v in dto_dict.items():
                setattr(coin, k, v)

        try:
            session.commit()
        except Exception as err:
            session.rollback()
            logger.error(err)


class CoinDTO(BaseModel):
    symbol: str = Field(alias="symbol", min_length=1)
    name: str = Field(alias="name", min_length=1)
    price: float = Field(alias="price")
    open: float = Field(alias="open")
    close: float | None = Field(alias="previousClose")
    changes_percentage: float | None = Field(alias="changesPercentage")
    change: float | None = Field(alias="change")
    day_low: float | None = Field(alias="dayLow")
    day_high: float | None = Field(alias="dayHigh")
    year_low: float | None = Field(alias="yearLow")
    year_high: float | None = Field(alias="yearHigh")
    market_cap: float | None = Field(alias="marketCap")
    avg_50: float | None = Field(alias="priceAvg50")
    avg_200: float | None = Field(alias="priceAvg200")
    volume: float | None = Field(alias="volume")
    avg_volume: float | None = Field(alias="avgVolume")
    shares: float | None = Field(alias="sharesOutstanding")
    api_timestamp: int = Field(alias="timestamp")

    @field_validator("api_timestamp")
    @classmethod
    def validate_api_time(cls, v):
        if abs(datetime.now() - datetime.fromtimestamp(v)) >= timedelta(minutes=60):
            raise ValueError("API time must be at least 60 minutes")
        return v

    @field_validator(
        "volume",
        "avg_volume",
        "shares",
        "market_cap",
        "avg_50",
        "avg_200",
        "year_low",
        "year_high",
        "day_low",
        "day_high",
        "changes_percentage",
        "change",
        "close",
    )
    @classmethod
    def replace_null_to_zero(cls, v):
        if v is None:
            return 0.0
        return v

    @field_validator("name", "symbol")
    @classmethod
    def trim_usd_suffix(cls, v):
        pattern = re.compile(r"\s*USD\s*$")
        result = re.sub(pattern, "", v)
        return result
