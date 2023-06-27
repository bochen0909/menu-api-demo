from fastapi import APIRouter, Depends, FastAPI

root_router = APIRouter()

app = FastAPI()

from .api.api_v1.endpoints import api_router as v1_api_router

app.include_router(v1_api_router )  # <----- API versioning

@app.get("/")
async def root():
    return {"message": "Hello, this is a demo of menu API."}