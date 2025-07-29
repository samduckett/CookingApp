from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..database import get_session
from ..models import Recipe
from ..crud import get_all, add_item, delete_item

router = APIRouter()

@router.get("/", response_model=list[Recipe])
def read_pantry(session: Session = Depends(get_session)):
    return get_all(session, Recipe)

@router.post("/", response_model=Recipe)
def create_pantry_item(item: Recipe, session: Session = Depends(get_session)):
    return add_item(session, item)

@router.delete("/{item_id}")
def remove_item(item_id: int, session: Session = Depends(get_session)):
    result = delete_item(session, Recipe, item_id)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": "Deleted"}
