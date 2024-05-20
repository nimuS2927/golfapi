from .admins import router as admins_router
from .tokens import router as tokens_router
from .middlwares import app_auth


app_auth.include_router(admins_router)
app_auth.include_router(tokens_router)

