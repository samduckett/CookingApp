from pydantic import BaseModel
from typing import Optional
import uuid

from app.schemas.ingredient import IngredientBase

class RecipeBase(BaseModel):
    name: str
    description: Optional[str]
    instructions: Optional[str]
    tags: Optional[list[str]]

class RecipeCreate(RecipeBase):
    ingredients: list[IngredientBase]

class Recipe(RecipeBase):
    id: uuid.UUID
    ingredients: list[IngredientBase] = []

    class Config:
        from_attributes = True