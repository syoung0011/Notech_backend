from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from schemas.users import UserRegRequest


async def reg_user(db:AsyncSession,user_data:UserRegRequest):
    user = User(username=user_data.username, password=user_data.password)
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user