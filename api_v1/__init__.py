from .users import router as users_router
from .middlwares import app_db


app_db.include_router(users_router)
