from fastapi import APIRouter
from app.api.v1.controller import teams_controller

api_router = APIRouter()

api_router.include_router(teams_controller.router, prefix="/teams", tags=["teams"])