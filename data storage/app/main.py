from fastapi import FastAPI
from app.database import Base, engine
from app.api import recipes, calendar, shopping_list

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Meal Planner API - Phase 1")

app.include_router(recipes.router)
app.include_router(calendar.router)
app.include_router(shopping_list.router)
