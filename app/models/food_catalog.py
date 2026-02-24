from app.core.database import Base
from sqlalchemy import ForeignKey, Text, Date, DateTime, func, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

class FoodCatalog(Base):
    __tablename__ = "food_catalog"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'), nullable=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    normal_macros: Mapped[dict] = mapped_column(JSONB, nullable=False)
