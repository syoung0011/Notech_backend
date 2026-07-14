from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud import users
from db.aiomysql import get_db
from models.users import User
from schemas.users import UserRegRequest, UserLoginRequest, UserProfileResponse
from utils.auth import encode_token, cur_user
from utils.exceptions import AppException
from utils.password import verify_password
from utils.responses import success_response

router = APIRouter(prefix="/users", tags=["用户"])

@router.post("/register", summary="用户注册")
async def register(user_data:UserRegRequest,db:AsyncSession=Depends(get_db)):
    ret=await users.get_user_by_username(db,user_data.username)
    if ret:
        raise AppException(msg="用户名已存在")
    await users.create_user(db,user_data)
    return success_response(msg="注册成功")
@router.post("/login", summary="用户登录")
async def login(user_data:UserLoginRequest,db:AsyncSession=Depends(get_db)):
    ret=await users.get_user_by_username(db,user_data.username)
    if not ret or not verify_password(user_data.password,ret.password):
        raise AppException(code=401,msg="用户名或密码错误")
    token=encode_token({"sub":str(ret.id)})
    return success_response(msg="登录成功",data={"token":token})
@router.get("/profile", summary="获取用户信息")
async def getProfile(user:User=Depends(cur_user),db:AsyncSession=Depends(get_db)):
    ret=await users.get_user_by_id(db,user.id)
    if not ret:
        raise AppException(msg="用户不存在")
    return success_response(msg="用户信息获取成功",data=UserProfileResponse.model_validate(ret).model_dump())

