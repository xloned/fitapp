from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.schedule_repo import get_day_entries, create_entry
from app.repositories.nutrition_repo import create_nutrition_log
from app.repositories.fitness_repo import create_workout
import datetime


async def get_today(session: AsyncSession, user_id: int):
    return await get_day_entries(session=session, user_id=user_id, date=datetime.date.today())

async def add_nutrition(session: AsyncSession, user_id: int, title: str,
                        macros: dict, mass: int, meal_type: str, food_id: int):
    nutrition_obj = await create_nutrition_log(session=session,
                                               user_id=user_id,
                                               date=datetime.date.today(),
                                               title=title,
                                               macros=macros,
                                               mass=mass,
                                               meal_type=meal_type,
                                               food_id=food_id)
    await create_entry(session=session,
                       user_id=user_id,
                       date=datetime.date.today(),
                       entry_type="nutrition",
                       title=title,
                       summary={"macros": macros,
                                "mass": mass,},
                       source_entity_id=nutrition_obj.id)

async def add_workout(session: AsyncSession, user_id: int, title: str):
    fitness_obj = await create_workout(session=session,
                                      user_id=user_id,
                                      date=datetime.date.today(),
                                      date=datetime.date.today(),
                                      title=title,)
    await create_entry(session=session,
                       user_id=user_id,
                       date=datetime.date.today(),
                       entry_type="fitness",
                       title=title,
                       summary={"exercises":[]},
                       source_entity_id=fitness_obj.id)