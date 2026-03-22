from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.db import add_user

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    # Добавить пользователя в БД
    add_user(
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.last_name
    )

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎯 Мои цели"), KeyboardButton(text="📊 Статистика целей")],
            [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="📁 Excel отчет")],
            [KeyboardButton(text="✏️ Редактировать"), KeyboardButton(text="🗑️ Сбросить данные")],
            [KeyboardButton(text="ℹ️ Справка")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "👋 Привет! Я бот для учета финансов И достижения целей.\\n\\n"
        "📝 КАК ПОЛЬЗОВАТЬСЯ:\\n"
        "• /add_goal - Добавить новую цель\\n"
        "• 🎯 Мои цели - Посмотреть цели на сегодня\\n"
        "• 📊 Статистика целей - Узнать прогресс\\n\\n"
        "Финансы:\\n"
        "• Введите: <категория> <сумма> - добавить расход\\n"
        "  Пример: еда 500\\n"
        "• Введите: зарплата 50000 - добавить доход\\n"
        "• Нажимайте кнопки для других функций",
        reply_markup=keyboard
    )


@router.message(lambda m: m.text == "ℹ️ Справка")
async def help_handler(message: types.Message):
    text = "📖 СПРАВКА:\\n\\n"
    text += "🎯 ЦЕЛИ:\\n"
    text += "• /add_goal - Добавить цель\\n"
    text += "• 🎯 Мои цели - Просмотреть цели\\n"
    text += "• 📊 Статистика целей - Статистика\\n\\n"
    
    text += "💳 РАСХОДЫ:\\n"
    text += "Введите: категория сумма\\n"
    text += "Примеры:\\n"
    text += "  еда 500\\n"
    text += "  такси 200\\n"
    text += "  покупка одежда 1500\\n\\n"

    text += "💰 ДОХОДЫ:\\n"
    text += "Введите: источник сумма\\n"
    text += "Примеры:\\n"
    text += "  зарплата 50000\\n"
    text += "  доход 10000\\n"
    text += "  фриланс 5000\\n\\n"

    text += "📊 ФУНКЦИИ:\\n"
    text += "• 📊 Статистика - смотреть расходы\\n"
    text += "• 📁 Excel - скачать отчет\\n"
    text += "• ✏️ Редактировать - изменить/удалить\\n"
    text += "• 🗑️ Сбросить - удалить все данные\\n"

    await message.answer(text)


def register(dp):
    dp.include_router(router)
