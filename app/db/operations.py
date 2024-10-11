from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.endpoints.users import UserRegister
from app.db import models

async def create_user(session: AsyncSession, user: UserRegister) -> models.User:
    db_user = models.User(**user.model_dump())
    db_user.logged = True
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

async def get_user(session: AsyncSession, id_: int) -> models.User:
    result = await session.execute(select(models.User).where(models.User.id == id_).limit(1))
    return result.scalar_one()

async def get_user_by_login(session: AsyncSession, login: str) -> models.User:
    result = await session.execute(select(models.User).where(models.User.login == login).limit(1))
    return result.scalar_one()

async def logout_user(session: AsyncSession, login: str) -> models.User:
    statement = update(models.User).where(models.User.login == login).values(
        {
            'logged': False
        }
    )
    await session.execute(statement)
    await session.commit()
    return