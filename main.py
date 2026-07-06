from fastapi import FastAPI
from routers.users import router as users_router
from utils.response import success_response
import uvicorn
app = FastAPI()
API_VER="/api/v1"
routers=[users_router,]
for router in routers:
    app.include_router(router, prefix=API_VER)
@app.get("/")
async def root():
    return success_response(msg="Hello World")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000,reload=True)

