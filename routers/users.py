from fastapi import APIRouter

from utils.response import success_response

router = APIRouter(prefix="/users", tags=["用户"])

@router.post("/register", summary="用户注册")
async def register():
    return success_response(msg="用户注册成功")
@router.post("/login", summary="用户登录")
async def login():
    return success_response(msg="用户登录成功")
