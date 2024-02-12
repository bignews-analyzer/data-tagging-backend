from fastapi import APIRouter

from api.api_v1.endpoints import item, user

api_router = APIRouter()
api_router.include_router(item.router, prefix="/item", tags=["item"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
