from typing import Annotated
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Form, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session
from app.api.schemas.user import UserRegister, UserLogin, User
from app.services.auth_service import AuthService
from app.core.security import get_current_user


auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


def get_auth_service(session: AsyncSession = Depends(get_async_session)) -> AuthService:
    return AuthService(session)


@auth_router.post('/register')
async def register_user(request: Request,
                        auth_service: AuthService = Depends(get_auth_service)):
    form_data = await request.form()
    registered_user = UserRegister(**form_data)
    return await auth_service.register(registered_user)


@auth_router.post('/login')
async def login_user(data: Annotated[OAuth2PasswordRequestForm, Depends()],
                     auth_service: AuthService = Depends(get_auth_service)):
    token = await auth_service.login(data)
    #response.headers['Authentication'] = 'Bearer ' + token
    return {
        'access_token': token,
        'token_type': 'Bearer',
        'logged_at': datetime.now(timezone.utc)
    }


@auth_router.get('/logout')
async def logout_user(current_user: Annotated[User, Depends(get_current_user)],
    auth_service: AuthService = Depends(get_auth_service)) -> dict:
    await auth_service.logout(current_user.login)
    return {
        'user': current_user.login,
        'status': 'logged out'
    }
