from fastapi import FastAPI
from api.api_v1.api import api_router
from core.config import settings
import models
from database.mysql_session import engine
from database.redis_session import redis_session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("shutdown")
async def shutdown_event():
    redis_session.close()
