from fastapi import APIRouter

from marvik_api.api import endpoints

api_router = APIRouter()
api_router.include_router(endpoints.router)
