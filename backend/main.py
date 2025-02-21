from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .dependencies import get_session, DBSession, lifespan
from .database import *
from .models import *

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

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/query")
def read_query(session: SessionDep):
    q = Select(Users).where(
        Condition().eq(Users.col("id"), 1)
    ).get_query().set_end()
    return {
        "query": q.construct_query(session)
    }
