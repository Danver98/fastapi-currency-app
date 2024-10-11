from fastapi import FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.schemas.user import UserRegister, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.db.database import get_async_session
from app.db import operations
from app.utils.singleton import Singleton
from app.core.security import hash_password, verify_password, create_jwt_token
from app.api.schemas import user
from app.core.config import settings
from app.api.schemas.currency import ExchangerRequest, ExchangerResponse, CurrencyListItem
from app.api.endpoints.errors.models import CurrencyExchangeError
from abc import ABC, abstractmethod
import aiohttp


class CurrencyService(ABC):
    """Abstract class for currency API"""
    __metaclass__ = Singleton
    BASE_URL: str = None
    ACCESS_KEY: str = None

    # def __init__(self, *args, **kwargs):
    #     headers = self._get_session_headers()
    #     print('Calling CurrencyService()/ Initializing session object...')
    #     if headers:
    #         self.session = aiohttp.ClientSession()
    #     else:
    #         self.session = aiohttp.ClientSession(headers=headers)
    #     print('Session object\'s been initialized')

    # async def __aenter__(self):
    #     return self

    # async def __aexit__(self, *args, **kwargs):
    #     await self.close()

    # async def close(self) -> None:
    #     if not self.session.closed:
    #         await self.session.close() 

    def _get_session_headers(self) -> dict:
        return {}

    @abstractmethod
    async def list(self, session: aiohttp.ClientSession) -> CurrencyListItem:
        raise NotImplementedError

    @abstractmethod
    async def exchange(self, session: aiohttp.ClientSession, exchanger: ExchangerRequest) -> ExchangerResponse:
        raise NotImplementedError


class APILayerCurrencyService(CurrencyService):
    BASE_URL = settings.APILAYER_URL
    ACCESS_KEY = settings.APILAYER_ACCESS_KEY

    def _get_session_headers(self) -> dict:
        return {
            'apikey': self.ACCESS_KEY
        }

    async def list(self, session: aiohttp.ClientSession) -> CurrencyListItem:
        url = self.BASE_URL + '/list'
        async with session.get(url, headers=self._get_session_headers()) as result:
            body = await result.json()
            return CurrencyListItem(**body)

    async def exchange(self, session: aiohttp.ClientSession, exchanger: ExchangerRequest) -> ExchangerResponse:
        url = self.BASE_URL + '/convert'
        params = {
            'amount': exchanger.amount,
            'from': exchanger.from_,
            'to': exchanger.to,
            'date': exchanger.date
        }
        async with session.get(url, params=params, headers=self._get_session_headers()) as result:
            body = await result.json()
            if not body.get('success'):
                raise CurrencyExchangeError(body.get('error'))
            response = ExchangerResponse(**body)
            return response


class ExchangeRateCurrencyService(CurrencyService):
    BASE_URL = settings.EXCHANGE_RATE_URL
    ACCESS_KEY = settings.EXCHANGE_RATE_ACCESS_KEY

    async def list(self, session: aiohttp.ClientSession) -> CurrencyListItem:
        url = self.BASE_URL + '/symbols'

    async def exchange(self, session: aiohttp.ClientSession, exchanger: ExchangerRequest) -> ExchangerResponse:
        pass