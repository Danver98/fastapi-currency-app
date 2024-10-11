from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.api.schemas.user import UserRegister, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.db import operations
from app.utils.singleton import Singleton
from app.core.security import hash_password, verify_password, create_jwt_token
from app.api.schemas import user

# class AuthService(metaclass=Singleton):
# We should create new service instance for each request (ain't good solution IMHO)
class AuthService():
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def register(self, data: UserRegister):
        data.password = hash_password(data.password)
        return await operations.create_user(self._session, data)

    async def get_user(self, id_: int):
        return await operations.get_user(self._session, id_)

    async def login(self, data: OAuth2PasswordRequestForm) -> str:
        db_user = await operations.get_user_by_login(self._session, data.username)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User nt found")
        if not verify_password(data.password, db_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Password")
        await operations.login_user(self._session, db_user.login)
        token_data = {
            'sub': db_user.login,
            'name': db_user.name,
            'surname': db_user.surname,
            'roles': db_user.roles
        }
        return create_jwt_token(token_data)

    async def logout(self, login: str):
        return await operations.logout_user(self._session, login)
