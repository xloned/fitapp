from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.schedule import Schedule
import datetime

async def get_day_entries(session: AsyncSession, user_id: int, date: datetime.date):
    result = await session.execute(
        select(Schedule)
        .where(Schedule.user_id == user_id)
        .where(Schedule.date == date)
        .order_by(Schedule.created_at)
    )
    return result.scalars().all()

async def delete_entry(session: AsyncSession, entry_id: int):
    await session.execute(
        delete(Schedule)
        .where(Schedule.id == entry_id)
    )
    await session.commit()

async def create_entry(session: AsyncSession, user_id: int, date: datetime.date, entry_type: str, title: str, summary: dict, source_entity_id: int):
    obj = Schedule(
        user_id=user_id,
        date=date,
        entry_type=entry_type,
        title=title,
        summary=summary,
        source_entity_id=source_entity_id
    )
    session.add(obj)
    await session.commit()
    return obj