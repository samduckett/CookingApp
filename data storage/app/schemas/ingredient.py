from pydantic import BaseModel
from typing import Optional

class IngredientBase(BaseModel):
    name: str
    quantity: float
    unit: Optional[str]
