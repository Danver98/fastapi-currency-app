from typing import Annotated
import aiohttp
from fastapi import APIRouter, Depends, Request
from app.services.currency_service import CurrencyService, APILayerCurrencyService, CurrencyListItem
from app.api.schemas.currency import ExchangerRequest, ExchangerResponse
from app.core.security import get_current_user


async def get_currency_service() -> CurrencyService:
    return APILayerCurrencyService()

async def get_session(request: Request) -> aiohttp.ClientSession:
    return request.app.aiohttp_client_session


currency_router = APIRouter(
    prefix="/currency",
    tags=["currency"],
    dependencies=[Depends(get_current_user)]
)


@currency_router.get('/list')
async def get_exchange_list(service: Annotated[CurrencyService, Depends(get_currency_service)],
                            session: Annotated[aiohttp.ClientSession, Depends(get_session)]) -> CurrencyListItem:
    """List of supported currencies"""
    return await service.list(session)


@currency_router.get('/exchange')
async def get_exchange_info(exchanger: ExchangerRequest,
                            service: Annotated[CurrencyService, Depends(get_currency_service)],
                            session: Annotated[aiohttp.ClientSession, Depends(get_session)]) -> ExchangerResponse:
    return await service.exchange(session, exchanger)