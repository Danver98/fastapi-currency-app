from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone

class ExchangerRequest(BaseModel):
    from_: str = Field(..., alias='from')
    to: list[str] | str
    amount: int = 1
    date: str = datetime.now(timezone.utc).strftime('%Y-%m-%d')


class CurrencyListItem(BaseModel):
    success: bool
    currencies: dict[str, str] = None


class Info(BaseModel):
    quote: float | None = None
    timestamp: datetime | None = datetime


class Query(BaseModel):
    amount: int | None = None
    from_: str | None = Field(default=None, alias='from')
    to: str | None = None


class ExchangerResponse(BaseModel):
    date: datetime | None = None
    historical: bool | None = None
    info: Info | None = None
    query: Query | None = None
    result: float | None = None
    success: bool | None = None
