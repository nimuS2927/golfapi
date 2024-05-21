from .users import router as users_router
from .tournaments import router as tournaments_router
from .holes import router as holes_router
from .flights import router as flights_router
from .middlwares import app_db


app_db.include_router(users_router)
app_db.include_router(tournaments_router)
app_db.include_router(holes_router)
app_db.include_router(flights_router)
