from fastapi import FastAPI
from .database import init_db
from .routers import pantry, recipes, cooklogs

app = FastAPI()

# Initialize SQLite tables
init_db()

# Include modular routers
app.include_router(pantry.router, prefix="/pantry", tags=["Pantry"])
app.include_router(recipes.router, prefix="/recipes", tags=["Recipes"])
app.include_router(cooklogs.router, prefix="/cooklogs", tags=["Cook Logs"])

print("FastAPI app initialized with modular routers for pantry, recipes, and cook logs.")