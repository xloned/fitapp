from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
import datetime

from app.repositories.user_repo import get_or_create_user
from app.repositories.schedule_repo import get_day_entries
from app.bot.keyboards import main_keyboard

router = Router()

DAY_NAMES = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
MONTH_NAMES = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля",
    5: "мая", 6: "июня", 7: "июля", 8: "августа",
    9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
}

from aiogram.enums import ParseMode

def format_day_text(date: datetime.date, entries: list) -> str:
    day_name = DAY_NAMES[date.weekday()]
    month = MONTH_NAMES[date.month]
    text = f"<blockquote expandable> 📅 {day_name} ~ {date.strftime('%d.%m')}\n\n"

    nutrition = [e for e in entries if e.entry_type == "nutrition"]
    fitness = [e for e in entries if e.entry_type == "fitness"]

    text += "🥗 <b>Питание</b>\n"
    if nutrition:
        for e in nutrition:
            text += f"  {e.title} </blockquote> \n"
    else:
        text += f"  — пусто — </blockquote> \n"

    text += "\n🏋️ <b>Тренировки</b>\n"
    if fitness:
        for e in fitness:
            text += f"  {e.title}\n </blockquote>"
    else:
        text += f" — \n </blockquote>"

    return text

def format_week_text(monday: datetime.date, entries_by_date: dict) -> str:
    text = ""
    for i in range(7):
        day = monday + datetime.timedelta(days=i)
        day_name = DAY_NAMES[day.weekday()]
        entries = entries_by_date.get(day, [])
        text += f"<blockquote expandable>📅 {day_name} ~ {day.strftime('%d.%m')}\n"
        if not entries:
            text += " — </blockquote>"
        else:
            for e in entries:
                text += f"  • {e.title}</blockquote>\n"
    return text

@router.message(Command("start"))
async def cmd_start(message: Message, session: AsyncSession):
    await get_or_create_user(session, message.from_user.id)
    today = datetime.date.today()
    entries = await get_day_entries(session, message.from_user.id, today)
    text = format_day_text(today, entries)
    await message.answer(text, reply_markup=main_keyboard(today, "day"), parse_mode=ParseMode.HTML)

@router.callback_query(lambda c: c.data.startswith("day:"))
async def show_day(callback: CallbackQuery, session: AsyncSession):
    date = datetime.date.fromisoformat(callback.data.split(":")[1])
    entries = await get_day_entries(session, callback.from_user.id, date)
    text = format_day_text(date, entries)
    await callback.message.edit_text(text, reply_markup=main_keyboard(date, "day"), parse_mode=ParseMode.HTML)
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("week:"))
async def show_week(callback: CallbackQuery, session: AsyncSession):
    date = datetime.date.fromisoformat(callback.data.split(":")[1])
    monday = date - datetime.timedelta(days=date.weekday())

    entries_by_date = {}
    for i in range(7):
        day = monday + datetime.timedelta(days=i)
        entries = await get_day_entries(session, callback.from_user.id, day)
        entries_by_date[day] = entries

    text = format_week_text(monday, entries_by_date)
    await callback.message.edit_text(text, reply_markup=main_keyboard(monday, "week"), parse_mode=ParseMode.HTML)
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("switch_to_day:"))
async def switch_to_day(callback: CallbackQuery, session: AsyncSession):
    date = datetime.date.fromisoformat(callback.data.split(":")[1])
    entries = await get_day_entries(session, callback.from_user.id, date)
    text = format_day_text(date, entries)
    await callback.message.edit_text(text, reply_markup=main_keyboard(date, "day"), parse_mode=ParseMode.HTML)
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("switch_to_week:"))
async def switch_to_week(callback: CallbackQuery, session: AsyncSession):
    date = datetime.date.fromisoformat(callback.data.split(":")[1])
    monday = date - datetime.timedelta(days=date.weekday())

    entries_by_date = {}
    for i in range(7):
        day = monday + datetime.timedelta(days=i)
        entries = await get_day_entries(session, callback.from_user.id, day)
        entries_by_date[day] = entries

    text = format_week_text(monday, entries_by_date)
    await callback.message.edit_text(text, reply_markup=main_keyboard(monday, "week"), parse_mode=ParseMode.HTML)
    await callback.answer()