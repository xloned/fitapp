from app.core.database import Base
from sqlalchemy import ForeignKey, Text, Date, DateTime, func, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
import datetime

class Nutrition(Base):
    __tablename__ = "nutrition_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'), nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    macros: Mapped[dict] = mapped_column(JSONB, nullable=False)
    mass: Mapped[int] = mapped_column(nullable=False)
    meal_type: Mapped[str] = mapped_column(Text, nullable=True)
    food_id: Mapped[int] = mapped_column(ForeignKey('food_catalog.id'), nullable=True)

