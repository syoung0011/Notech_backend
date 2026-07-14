from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from schemas.users import UserRegRequest
from utils.password import hash_password


async def get_user_by_username(db:AsyncSession,username:str):
    stmt=select(User).where(User.username==username)
    res=await db.execute(stmt)
    return res.scalar_one_or_none()

async def get_user_by_id(db:AsyncSession,id:int):
    stmt=select(User).where(User.id==id)
    res=await db.execute(stmt)
    return res.scalar_one_or_none()

async def create_user(db:AsyncSession, user_data:UserRegRequest):
    user = User(
        username=user_data.username,
        password=hash_password(user_data.password)
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user