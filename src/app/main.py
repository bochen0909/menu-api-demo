from .api.api_v1.endpoints import api_router as v1_api_router
from fastapi import APIRouter, Depends, FastAPI

root_router = APIRouter()

app = FastAPI()


app.include_router(v1_api_router)  # <----- API versioning


@app.get("/")
async def root():
    return {"message": "Hello, this is a demo application for restaurant API."}
