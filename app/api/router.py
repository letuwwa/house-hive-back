from fastapi import APIRouter
from app.api.v1 import auth_router, house_member_router, house_router


api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(house_router)
api_router.include_router(house_member_router)
