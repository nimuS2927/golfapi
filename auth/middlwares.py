from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from core.config import c_project

# http_bearer = HTTPBearer(auto_error=False)
# app_auth = FastAPI(dependencies=[Depends(http_bearer)])
app_auth = FastAPI()

# Some middlewares ...
# @app_auth.middleware("http")
# async def middleware_api_v1(request: Request, call_next):
#     access_token = request.headers.get('X-Auth-Access-Token')
#     if access_token:
#         response = await call_next(request)
#         return response
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"Invalid headers"
#     )
