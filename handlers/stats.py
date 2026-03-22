# handlers/stats.py (БЕЗ EXCEL)
from aiogram import types, Router
from database.db import get_expenses, get_all

router = Router()

@router.message(lambda m: m.text == "💰 Статистика расходов")
async def stats_handler(message: types.Message):
    """Показать статистику расходов"""
    data = get_expenses(message.from_user.id)

    if not data:
        await message.answer("Нет данных")
        return

    text = "📊 Расходы по категориям:\n\n"
    total = 0

    for cat, amount in data:
        text += f"💳 {cat} — {amount} сўм\n"
        total += amount

    text += f"\n💰 Всего: {total} сўм"

    await message.answer(text)

def register(dp):
    dp.include_router(router)
