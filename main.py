from fastapi import FastAPI
from api.api_v1.api import api_router
from core.config import settings
import models
from database.session import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router, prefix=settings.API_V1_STR)
