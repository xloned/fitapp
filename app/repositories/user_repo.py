from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.user import User

async def get_or_create_user(session, telegram_id):
    result = await session.execute(
        select(User)
        .where(User.tg_id == telegram_id)
    )
    user = result.scalar_one_or_none()
    if user == None:
        user = User(tg_id=telegram_id)
        session.add(user)
        await session.commit()
    return result