from fastapi import FastAPI,Request,status
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError


class AppException(Exception):
    def __init__(self, code:int=400,msg:str="业务异常"):
        self.msg = msg
        self.code=code
        super().__init__(self.msg)

def register_exception_handlers(app:FastAPI, logger):
    @app.exception_handler(AppException)
    async def _app_exception_handler(request: Request, exc: AppException):
        logger.error(f"❌ 业务异常: {exc.msg}")
        return JSONResponse(
            status_code=exc.code,
            content={"code": exc.code, "msg": exc.msg, "data": None},
        )

    @app.exception_handler(RequestValidationError)
    async def _validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = []
        for e in exc.errors():
            field = " -> ".join(str(loc) for loc in e.get("loc", []))
            errors.append(f"字段[{field}]: {e.get('msg', '校验失败')}")
        logger.error(f"❌ 参数校验失败: {errors}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"code": 422, "msg": "参数校验失败", "data": errors},
        )

    @app.exception_handler(SQLAlchemyError)
    async def _database_exception_handler(request: Request, exc: SQLAlchemyError):
        logger.error(f"❌ 数据库操作异常: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"code": 500, "msg": "数据库操作异常", "data": None},
        )

    @app.exception_handler(HTTPException)
    async def _http_exception_handler(request: Request, exc: HTTPException):
        logger.error(f"❌ HTTP异常: {exc.status_code} {exc.detail} {exc.headers}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"code": exc.status_code, "msg": exc.detail, "data": exc.headers},
        )

    @app.exception_handler(Exception)
    async def _general_exception_handler(request: Request, exc: Exception):
        logger.error(f"❌ 未知异常: {type(exc).__name__} {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"code": 500, "msg": f"未知异常: {type(exc).__name__}", "data": f"{exc}"},
        )
