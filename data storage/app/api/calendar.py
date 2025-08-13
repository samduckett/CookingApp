# --------------------------- Import Statements ---------------------------
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from typing import Optional, cast
from datetime import date

from app.database import get_db

# --------------------------- Router Setup ---------------------------
from app.models.meal_calendar import MealCalendar as meal_calendar_model
from app.models.recipe import Recipe as recipe_model

from app.schemas import meal_calendar as meal_calendar_schemas

router = APIRouter(prefix="/calendar", tags=["Meal Calendar"])

# --------------------------- API Endpoints ---------------------------
# Get meals for a date range
@router.get("/", response_model=list[meal_calendar_schemas.MealCalendar])
def get_meals(
    start: Optional[date] = Query(None, description="Start date (inclusive)"),
    end: Optional[date] = Query(None, description="End date (inclusive)"),
    db: Session = Depends(get_db),
):
    """Retrieve meals within a specified date range.
    If no dates are provided, all meals will be returned."""
    
    # Validate date inputs
    if start and not isinstance(start, date):
        raise HTTPException(status_code=400, detail="Start date must be a valid date")
    if end and not isinstance(end, date):
        raise HTTPException(status_code=400, detail="End date must be a valid date")
    if start and end and start > end:
        raise HTTPException(status_code=400, detail="Start date cannot be after end date")

    # Query meals based on date range
    query = db.query(meal_calendar_model)
    if start:
        query = query.filter(meal_calendar_model.date >= start)
    if end:
        query = query.filter(meal_calendar_model.date <= end)
        
    return query.order_by(meal_calendar_model.date).all()

# Add a new meal
@router.post("/", response_model=meal_calendar_schemas.MealCalendar)
def add_meal(meal: meal_calendar_schemas.MealCalendarCreate, db: Session = Depends(get_db)):
    """Add a new meal to the calendar."""
    
    recipe = db.query(recipe_model).filter(recipe_model.id == meal.recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db_meal = meal_calendar_model(
        date=meal.date,
        meal_type=meal.meal_type,
        recipe_id=meal.recipe_id,
        notes=meal.notes
    )
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal

@router.put("/{meal_id}", response_model=meal_calendar_schemas.MealCalendar)
def update_meal(meal_id: str, meal: meal_calendar_schemas.MealCalendarUpdate, db: Session = Depends(get_db)):
    
    db_meal: meal_calendar_model = db.query(meal_calendar_model).filter(meal_calendar_model.id == meal_id).first()
    if not db_meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    # Optional update fields
    if meal.date is not None:
        db_meal.date = meal.date 
    if meal.meal_type is not None:
        db_meal.meal_type = meal.meal_type
    if meal.recipe_id is not None:
        # Verify recipe exists
        recipe = db.query(recipe_model).filter(recipe_model.id == meal.recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        db_meal.recipe_id = meal.recipe_id
    if meal.notes is not None:
        db_meal.notes = meal.notes

    db.commit()
    db.refresh(db_meal)
    return db_meal

@router.delete("/{meal_id}", status_code=204)
def delete_meal(meal_id: str, db: Session = Depends(get_db)):
    db_meal = db.query(meal_calendar_model).filter(meal_calendar_model.id == meal_id).first()
    if not db_meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    db.delete(db_meal)
    db.commit()
