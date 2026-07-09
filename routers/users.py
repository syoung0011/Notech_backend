from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud import users
from db.aiomysql import get_db
from schemas.users import UserRegRequest
from utils.response import success_response

router = APIRouter(prefix="/users", tags=["用户"])

@router.post("/register", summary="用户注册")
async def register(user_data:UserRegRequest,db:AsyncSession=Depends(get_db)):
    ret=await users.reg_user(db,user_data)
    return success_response(msg="用户注册成功",data=ret)
@router.post("/login", summary="用户登录")
async def login():
    return success_response(msg="用户登录成功")