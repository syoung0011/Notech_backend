from datetime import timedelta, datetime, timezone
from typing import Optional

from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jwt import encode, decode
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import settings
from db.aiomysql import get_db
from models.users import User

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str)->bool:
    return pwd_context.verify(plain_password, hashed_password)

def encode_token(data:dict,expires_delta:Optional[timedelta]=None)->str:
    to_encode=data.copy()
    expire=(datetime.now(timezone.utc) +
            (expires_delta if expires_delta else timedelta(hours=settings.jwt.hour_delta)))
    to_encode.update({'exp':expire})
    encoded=encode(to_encode,settings.jwt.secret_key,algorithm=settings.jwt.algorithm)
    return encoded

def decode_token(token:str)->dict:
    try:
        payload=decode(token,settings.jwt.secret_key,algorithms=[settings.jwt.algorithm])
        return payload
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 无效或已过期",
            headers={"WWW-Authenticate": "Bearer"}
        )

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="")
async def cur_user(token:str=Depends(oauth2_scheme),db:AsyncSession=Depends(get_db))->User:
    payload=decode_token(token)
    user_id=payload.get('sub')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 中缺少用户标识",
            headers={"WWW-Authenticate": "Bearer"}
        )
    stmt=select(User).where(User.id==user_id)
    res=await db.execute(stmt)
    res=res.scalar_one_or_none()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="持有该Token的用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return res