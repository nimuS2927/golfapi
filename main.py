from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

# from api_v1 import app_db
# from auth import app_auth
from core import c_project


@asynccontextmanager
async def lifespan(app_: FastAPI):

    yield


app = FastAPI(lifespan=lifespan)

# app.mount(c_project.api_v1_prefix, app_db)
# app.mount(c_project.auth_v1_prefix, app_auth)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        reload=True,
        host='localhost',
    )
