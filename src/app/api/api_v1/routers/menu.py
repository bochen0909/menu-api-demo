from fastapi import APIRouter, HTTPException, Path, Depends, Query 
from app.dependencies import get_dao
router = APIRouter()


@router.get("/restaurant/{restaurant_id}")
async def find_restaurant_by_id(restaurant_id:str, dao=Depends(get_dao)):
    return dao.find_customer(restaurant_id)

@router.get("/food/{food_term}")
async def find_restaurants_by_food_term(food_term:str, limit: int = Query(10, ge=1), dao=Depends(get_dao)):
    return dao.find_food_term(food_term, limit)

