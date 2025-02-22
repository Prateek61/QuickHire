from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .dependencies import get_session, DBSession, lifespan, get_token_from_header

from typing import Union, Annotated, Optional

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from . import routers

app.include_router(routers.router)
