from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth.tokens.utils import decode_jwt
from core.config import c_project


http_bearer = HTTPBearer(auto_error=False)
app_db = FastAPI(dependencies=[Depends(http_bearer)])


@app_db.middleware("http")
async def middleware_api_v1(
        request: Request,
        call_next,
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Invalid headers"
    )
    path = request.url.path
    if path.endswith('docs') or path.endswith('docs/') or path.endswith('openapi.json'):
        response = await call_next(request)
        return response
    else:
        try:
            credentials = request.headers.get('Authorization'),
            scheme, token_str = credentials[0].split()
            if token_str:
                token = decode_jwt(token_str)
                if token[c_project.auth_jwt.token_type_field] == c_project.auth_jwt.access_token_type:
                    response = await call_next(request)
                    return response
            raise unauthed_exc
        except AttributeError:
            raise unauthed_exc
