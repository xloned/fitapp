import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import async_session_factory
from app.bot.handlers.diary import router

async def get_session():
    async with async_session_factory() as session:
        yield session

async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(router)

    # middleware для передачи сессии в handlers
    from aiogram import BaseMiddleware
    from typing import Callable, Awaitable, Any
    from aiogram.types import TelegramObject

    class SessionMiddleware(BaseMiddleware):
        async def __call__(self, handler: Callable[[TelegramObject, dict], Awaitable[Any]], event: TelegramObject, data: dict) -> Any:
            async with async_session_factory() as session:
                data["session"] = session
                return await handler(event, data)

    dp.update.middleware(SessionMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())