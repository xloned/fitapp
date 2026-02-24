from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime

def main_keyboard(date: datetime.date, mode: str) -> InlineKeyboardMarkup:
    today = datetime.date.today()

    if mode == "day":
        prev_date = date - datetime.timedelta(days=1)
        next_date = date + datetime.timedelta(days=1)
        switch_text = "📅 Неделя"
        switch_callback = f"switch_to_week:{date.isoformat()}"
    else:  # week
        prev_date = date - datetime.timedelta(days=7)
        next_date = date + datetime.timedelta(days=7)
        switch_text = "📆 День"
        switch_callback = f"switch_to_day:{date.isoformat()}"

    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="◀️", callback_data=f"{mode}:{prev_date.isoformat()}"),
        InlineKeyboardButton(text="🗓 Сегодня", callback_data=f"{mode}:{today.isoformat()}"),
        InlineKeyboardButton(text=switch_text, callback_data=switch_callback),
        InlineKeyboardButton(text="▶️", callback_data=f"{mode}:{next_date.isoformat()}"),
    ]])