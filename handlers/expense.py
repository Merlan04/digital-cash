# handlers/expense.py (С СУММАМИ)
from aiogram import types, Router
from datetime import datetime
from database.db import add_transaction
from utils.categories import detect_category

router = Router()

def is_expense_format(message: types.Message) -> bool:
    """Проверяет фо��мат: категория сумма"""
    if message.text.startswith("/"):
        return False
    if message.text.startswith("🎯"):
        return False

    text = message.text.split()
    if len(text) < 2:
        return False

    try:
        amount = int(text[-1])
        if amount <= 0:
            return False
        if amount > 10000000:
            return False
        return True
    except ValueError:
        return False

@router.message(lambda m: is_expense_format(m))
async def add_expense(message: types.Message):
    try:
        text = message.text.split()
        amount = int(text[-1])
        category_text = " ".join(text[:-1])

        category = detect_category(category_text)

        add_transaction(
            message.from_user.id,
            "expense",
            category,
            amount,
            datetime.now().strftime("%Y-%m-%d")
        )

        await message.answer(f"✅ Расход записан: {category} - {amount} сўм")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")

def register(dp):
    dp.include_router(router)
