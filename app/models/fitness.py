from app.core.database import Base
from sqlalchemy import ForeignKey, Text, Date, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column
import datetime

class FitnessWorkout(Base):
    __tablename__ = "workout_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)


class WorkoutSet(Base):
    __tablename__ = "workout_sets"

    id: Mapped[int] = mapped_column(primary_key=True)
    exercise: Mapped[str] = mapped_column(Text, nullable=False) # название
    reps: Mapped[int] = mapped_column(nullable=False) # повторы
    sets_count: Mapped[int] = mapped_column(nullable=False) # подходы
    weight: Mapped[float] = mapped_column(Float, nullable=False) # вес, процентаж или килограммы
    done: Mapped[bool] = mapped_column(Boolean) # отметка после выполнения
    workout_id: Mapped[int] = mapped_column(ForeignKey('workout_logs.id'), nullable=False) # связь с тренировкой