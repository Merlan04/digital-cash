from aiogram import types, Router
from database.db import get_expenses, get_all
from utils.excel import create_excel

router = Router()

@router.message(lambda m: m.text == "📊 Статистика")
async def stats(message: types.Message):
    data = get_expenses(message.from_user.id)

    if not data:
        await message.answer("Нет данных")
        return

    text = "📊 Расходы по категориям:\n\n"
    total = 0

    for cat, amount in data:
        text += f"💳 {cat} — {amount}₽\n"
        total += amount

    text += f"\n💰 Всего: {total}₽"

    await message.answer(text)

@router.message(lambda m: m.text == "📁 Excel отчет")
async def excel(message: types.Message):
    try:
        file = create_excel(message.from_user.id)

        if file:
            with open(file, "rb") as f:
                await message.answer_document(f, caption="📊 Ваш отчет")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")

def register(dp):
    dp.include_router(router)