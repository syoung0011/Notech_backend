import time

from fastapi import FastAPI,Request
from starlette.middleware.cors import CORSMiddleware


def register_middleware(app: FastAPI,logger)->None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def _logging_middleware(request: Request, call_next):
        start=time.time()
        response = await call_next(request)
        end=time.time()
        process_ms = round((end - start) * 1000, 2)
        method=request.method
        url=str(request.url)
        ip = request.client.host if request.client else "unknown"
        params = str(request.query_params) if request.query_params else ""
        msg = (
            f"{method} {url} | IP: {ip} | Params: {params} | "
            f"Status: {response.status_code} | Time: {process_ms}ms"
        )
        if response.status_code >= 400:
            logger.warning(msg)
        else:
            logger.info(msg)
        return response