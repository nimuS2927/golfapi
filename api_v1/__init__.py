from .scores.schemas import *
from .flights.schemas import *
from .users.schemas import *
from .holes.schemas import *
from .totalscores.schemas import *
from .tournaments.schemas import *

from .users import router as users_router
from .flights import router as flights_router
from .holes import router as holes_router
from .scores import router as scores_router
from .totalscores import router as totalscores_router
from .tournaments import router as tournaments_router
from .middlwares import app_db


app_db.include_router(users_router)
app_db.include_router(tournaments_router)
app_db.include_router(holes_router)
app_db.include_router(scores_router)
app_db.include_router(totalscores_router)
app_db.include_router(flights_router)
