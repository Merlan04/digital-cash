# handlers/income.py (ИСПРАВЛЕННЫЙ)
from aiogram import types, Router
from datetime import datetime
from database.db import add_transaction
from utils.categories import detect_category

router = Router()

def is_income_format(message: types.Message) -> bool:
    """Проверяет формат дохода"""
    text = message.text.split()
    if len(text) < 2:
        return False
    try:
        amount = int(text[-1])
        if amount <= 0 or amount > 10000000:
            return False
        return True
    except ValueError:
        return False

@router.message(lambda m: is_income_format(m))
async def add_income(message: types.Message):
    try:
        text = message.text.split()
        amount = int(text[-1])
        category_text = " ".join(text[:-1])

        category = detect_category(category_text)

        add_transaction(
            message.from_user.id,
            "income",
            category,
            amount,
            datetime.now().strftime("%Y-%m-%d")
        )

        await message.answer(f"✅ Доход записан: {category} - {amount} сўм")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")

def register(dp):
    dp.include_router(router)
