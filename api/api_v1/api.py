from fastapi import APIRouter

from api.api_v1.endpoints import data, user

api_router = APIRouter()
api_router.include_router(data.router, prefix="/data", tags=["data"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
