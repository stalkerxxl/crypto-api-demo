from enum import Enum


class CoinFields(str, Enum):
    price = "price"
    market_cap = "market_cap"
    volume = "volume"
    avg_volume = "avg_volume"
    day_low = 'day_low'
    day_high = 'day_high'
    year_low = 'year_low'
    year_high = 'year_high'
    changes_percentage = "changes_percentage"
    change = 'change'
    avg_50 = 'avg_50'
    avg_200 = 'avg_200'
    shares = 'shares'


class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"
