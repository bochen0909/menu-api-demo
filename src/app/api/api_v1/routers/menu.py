from fastapi import APIRouter, HTTPException, Path, Depends, Query 
from app.dependencies import get_dao
router = APIRouter()


@router.get("/restaurant/{restaurant_id}")
async def find_restaurant_by_id(restaurant_id:str, dao=Depends(get_dao)):
    """
    Find a restaurant by ID.

    Args:
        restaurant_id (str): The ID of the restaurant to retrieve.

    Returns:
        dict: name, location data, and menu URL
    """
    return dao.find_customer(restaurant_id)

@router.get("/food/{food_term}")
async def find_restaurants_by_food_term(food_term:str, limit: int = Query(10, ge=1), dao=Depends(get_dao)):
    """
    Find restaurants that have the food term in their website.

    Args:
        food_term (int): the term to search.

    Returns:
        dict: restaurant ids and rank scores
    """
    return dao.find_food_term(food_term, limit)

