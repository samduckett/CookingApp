# --------------------------- Import Statements ---------------------------
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db

# --------------------------- Router Setup ---------------------------
from app.models.recipe import Recipe as recipe_model
from app.models.ingredient import Ingredient as ingredient_model

from app.schemas import recipe as recipe_schemas

router = APIRouter(prefix="/recipes", tags=["Recipes"])

# --------------------------- API Endpoints ---------------------------
# Get all recipes
@router.get("/", response_model=list[recipe_schemas.Recipe])
def get_recipes(db: Session = Depends(get_db)):
    return db.query(recipe_model).all()

# Get a recipe by ID
@router.get("/{recipe_id}", response_model=recipe_schemas.Recipe)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(recipe_model).filter(recipe_model.id == recipe_id).first()
    
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    return recipe

# Create a new recipe
@router.post("/", response_model=recipe_schemas.Recipe)
def create_recipe(recipe: recipe_schemas.RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = recipe_model(
        name=recipe.name,
        description=recipe.description,
        instructions=recipe.instructions,
        tags=recipe.tags
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    for ingredient in recipe.ingredients:
        db_ing = ingredient_model(
            recipe_id=db_recipe.id,
            name=ingredient.name,
            quantity=ingredient.quantity,
            unit=ingredient.unit
        )
        db.add(db_ing)
    db.commit()
    return db_recipe
