from sqlmodel import Session, select
from .models import Recipe, PantryItem, CookLog

def get_all(session: Session, model):
    return session.exec(select(model)).all()

def get_by_id(session: Session, model, item_id: int):
    return session.get(model, item_id)

def add_item(session: Session, item):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

def delete_item(session: Session, model, item_id: int):
    item = session.get(model, item_id)
    if item:
        session.delete(item)
        session.commit()
    return item
