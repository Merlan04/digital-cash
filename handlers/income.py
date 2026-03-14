from aiogram import types, Router
from datetime import datetime
from database.db import add_transaction

router = Router()

income_words = ["зарплата", "доход", "фриланс"]

def is_income_format(message: types.Message) -> bool:
    """Проверяет формат: источник сумма"""
    text = message.text.split()
    if len(text) != 2:
        return False
    if text[0] not in income_words:
        return False
    try:
        int(text[1])
        return True
    except ValueError:
        return False

@router.message(lambda m: is_income_format(m))
async def add_income(message: types.Message):
    text = message.text.split()
    source, amount = text
    amount = int(amount)

    add_transaction(
        message.from_user.id,
        "income",
        source,
        amount,
        datetime.now().strftime("%Y-%m-%d")
    )

    await message.answer("💰 Доход добавлен")

def register(dp):
    dp.include_router(router)