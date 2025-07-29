from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, JSON

class Ingredient(SQLModel):
    name: str
    quantity: float
    unit: str
    allergens: Optional[List[str]] = []

class Recipe(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str

    # Store complex fields as JSON
    ingredients: List[dict] = Field(sa_column=Column(JSON))
    steps: List[str] = Field(sa_column=Column(JSON))
    
    base_servings: int

class PantryItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    quantity: float
    unit: str

class CookLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    recipe_id: int
    cooked_at: datetime
    time_taken_minutes: Optional[int]
    rating: Optional[int]
