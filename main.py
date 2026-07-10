from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.aiomysql import create_tables
from routers.users import router as users_router
from utils.exceptions import register_exception_handlers
from utils.loggers import logger
from utils.responses import success_response
from utils.middlewares import register_middlewares

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
register_middlewares(app,logger)
register_exception_handlers(app,logger)

API_VER="/api/v1"
routers=[users_router,]
for router in routers:
    app.include_router(router, prefix=API_VER)
@app.get("/")
async def root():
    return success_response(msg="Hello World")