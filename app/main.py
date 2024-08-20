from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import get_db, engine
from . import models
from .router import user, auth

models.Base.metadata.create_all(bind = engine)
app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)


