from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..database import get_session
from ..models import PantryItem
from ..crud import get_all, add_item, delete_item

router = APIRouter()

@router.get("/", response_model=list[PantryItem])
def read_pantry(session: Session = Depends(get_session)):
    return get_all(session, PantryItem)

@router.post("/", response_model=PantryItem)
def create_pantry_item(item: PantryItem, session: Session = Depends(get_session)):
    return add_item(session, item)

@router.delete("/{item_id}")
def remove_item(item_id: int, session: Session = Depends(get_session)):
    result = delete_item(session, PantryItem, item_id)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": "Deleted"}
