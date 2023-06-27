from fastapi import APIRouter

from app.api.api_v1.routers import menu


api_router = APIRouter()
api_router.include_router(menu.router, prefix="/v1", tags=["menu"])