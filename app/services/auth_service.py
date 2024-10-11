from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.user import UserRegister
from app.db import operations
from app.core.security import hash_password, verify_password, create_jwt_token

# class AuthService(metaclass=Singleton):
# We should create new service instance for each request (ain't good solution IMHO)
class AuthService():
    """
        Service class for working with users
    """
    def __init__(self, session: AsyncSession):
        self._session = session

    async def register(self, data: UserRegister):
        """Register user method"""
        data.password = hash_password(data.password)
        return await operations.create_user(self._session, data)

    async def get_user(self, id_: int):
        """Get user method"""
        return await operations.get_user(self._session, id_)

    async def login(self, data: OAuth2PasswordRequestForm) -> str:
        """Login user method"""
        db_user = await operations.get_user_by_login(self._session, data.username)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
        # if db_user.logged:
        #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User's already been authenticated")
        if not verify_password(data.password, db_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Password")
        token_data = {
            'sub': db_user.login,
            'name': db_user.name,
            'surname': db_user.surname,
            'roles': db_user.roles
        }
        # login_user will commit changes what'll cause session's objects expiration and their attributes'll be loaded from db
        # again at next invokation to them. Can be circumvented by using Session.expire_on_commit=False
        await operations.login_user(self._session, db_user.login)
        return create_jwt_token(token_data)

    async def logout(self, login: str):
        """Logout user method"""
        return await operations.logout_user(self._session, login)
