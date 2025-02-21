from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .dependencies import get_session, DBSession, lifespan 

from typing import Union, Annotated

# Dependency
SessionDep = Annotated[DBSession, Depends(get_session)]

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from . import routers

app.include_router(routers.router)
