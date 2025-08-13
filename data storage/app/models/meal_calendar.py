from sqlalchemy import Column, String, Date, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base

class MealCalendar(Base):
    __tablename__ = "meal_calendar"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(Date, nullable=False)
    meal_type = Column(String, nullable=False)
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id", ondelete="CASCADE"))
    notes = Column(Text)
