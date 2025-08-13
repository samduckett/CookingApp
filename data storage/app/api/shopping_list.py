# --------------------------- Import Statements ---------------------------
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from typing import List, Dict, Optional
from datetime import date

from app.database import get_db

# --------------------------- Router Setup ---------------------------
from app.models.meal_calendar import MealCalendar as meal_calendar_model
from app.models.ingredient import Ingredient as ingredient_model

from app.schemas import ingredient as ingredient_schemas

router = APIRouter(prefix="/shopping-list", tags=["Shopping List"])

# --------------------------- API Endpoints ---------------------------
# Get shopping list for a date range
@router.get("/", response_model=List[ingredient_schemas.IngredientBase])
def get_shopping_list(
    start: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    # Get meals in the date range
    meals = db.query(meal_calendar_model).filter(
        meal_calendar_model.date >= start,
        meal_calendar_model.date <= end,
    ).all()

    recipe_ids = {meal.recipe_id for meal in meals}
    if not recipe_ids:
        return []

    # Get ingredients for these recipes
    ingredients: List[ingredient_model]= db.query(ingredient_model).filter(
        ingredient_model.recipe_id.in_(recipe_ids)
    ).all()
    
    # Aggregate by name+unit
    aggregated = {}

    for ingredient in ingredients:
        key = (ingredient.name.lower())
        aggregated[key]["quantity"] += float(str(ingredient.quantity))
        aggregated[key]["unit"] = ingredient.unit

    # Prepare response list
    shopping_list = []
    for (name, unit), data in aggregated.items():
        shopping_list.append(ingredient_schemas.IngredientBase(
            name=name,
            quantity=data["quantity"],
            unit=data["unit"]
        ))

    return shopping_list
