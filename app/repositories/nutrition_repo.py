from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.nutrition import Nutrition
import datetime

async def get_day_nutrition(session: AsyncSession, user_id: int, date: datetime.date):
    result = await session.execute(
        select(Nutrition)
        .where(Nutrition.user_id == user_id)
        .where(Nutrition.date == date)
        .order_by(Nutrition.created_at)
    )
    return result.scalars().all()

async def delete_nutrition_log(session: AsyncSession, entry_id: int):
    await session.execute(
        delete(Nutrition)
        .where(Nutrition.id == entry_id)
    )
    await session.commit()

async def create_nutrition_log(session: AsyncSession, user_id: int, date: datetime.date, title: str, macros: dict, mass: int, meal_type: str, food_id: int = None):
    obj = Nutrition(
        user_id=user_id,
        date=date,
        title=title,
        macros = macros,
        mass = mass,
        meal_type = meal_type,
        food_id = food_id
    )
    session.add(obj)
    await session.commit()
    return obj