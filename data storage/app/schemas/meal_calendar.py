from pydantic import BaseModel
from typing import Optional
from datetime import date
import uuid

class MealCalendarBase(BaseModel):
    date: date
    meal_type: str
    recipe_id: uuid.UUID
    notes: Optional[str]

class MealCalendarCreate(MealCalendarBase):
    pass

class MealCalendarUpdate(BaseModel):
    date: Optional[date]
    meal_type: Optional[str]
    recipe_id: Optional[uuid.UUID]
    notes: Optional[str]

class MealCalendar(MealCalendarBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
