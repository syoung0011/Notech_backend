from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.aiomysql import create_tables
from routers.users import router as users_router
from utils.loggers import api_logging
from utils.response import success_response
from utils.middleware import register_middleware

logger = api_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await create_tables()
        logger.info("✅ 建表成功")
    except Exception as e:
        logger.error(f"❌ 建表失败: {e}")
    yield
    logger.info("✅ 应用关闭")
app = FastAPI(lifespan=lifespan)
register_middleware(app,logger)

API_VER="/api/v1"
routers=[users_router,]
for router in routers:
    app.include_router(router, prefix=API_VER)
@app.get("/")
async def root():
    return success_response(msg="Hello World")