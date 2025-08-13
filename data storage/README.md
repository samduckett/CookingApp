## MVP Scope

**Features:**
- Create, edit, delete recipes
- Store ingredients per recipe
- Weekly meal calendar
- Assign recipes to days
- Basic shopping list (ingredients from all recipes in the week)

---
## Database Schema (PostgreSQL)

### **1. `recipes`**
- **id** — UUID (PK), `gen_random_uuid()`
- **name** — TEXT, recipe name
- **description** — TEXT, optional notes
- **instructions** — TEXT, cooking steps
- **tags** — TEXT[], e.g., `{quick,vegetarian}`
- **created_at** — TIMESTAMP, default now()
- **updated_at** — TIMESTAMP, auto-update

### **2. `ingredients`**
- **id** — UUID (PK)
- **recipe_id** — UUID (FK), links to `recipes.id`
- **name** — TEXT, ingredient name
- **quantity** — NUMERIC, amount (can store as decimal)
- **unit** — TEXT, e.g., `g`, `ml`, `cup`

### **3. `meal_calendar`**
- **id** — UUID (PK)
- **date** — DATE, day the meal is planned
- **meal_type** — TEXT, e.g., `breakfast`, `lunch`, `dinner`
- **recipe_id** — UUID (FK), recipe assigned
- **notes** — TEXT, optional

---
## API Endpoints (FastAPI)

### **Recipes**
- `GET /recipes` → List all recipes
- `GET /recipes/{id}` → Get recipe details (with ingredients)
- `POST /recipes` → Create recipe (with ingredients array)
- `PUT /recipes/{id}` → Update recipe (and ingredients)
- `DELETE /recipes/{id}` → Delete recipe

### **Meal Calendar**
- `GET /calendar?start=YYYY-MM-DD&end=YYYY-MM-DD` → Get meals in date range
- `POST /calendar` → Add meal to a date
- `PUT /calendar/{id}` → Update meal
- `DELETE /calendar/{id}` → Remove meal from calendar

### **Shopping List**
- `GET /shopping-list?start=YYYY-MM-DD&end=YYYY-MM-DD`  
    → Aggregates ingredients from recipes in date range into one list  
    → Groups by ingredient name + sums quantities if units match