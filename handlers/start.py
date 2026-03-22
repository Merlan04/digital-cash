# handlers/start.py (ОБНОВЛЁННЫЙ)
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    """Команда /start"""
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "💰 Добро пожаловать в Finance Bot!\n\n"
        "Я помогу тебе отслеживать доходы и расходы в сўм.\n"
        "Учи цели, играй в игры и становись финансово грамотнее!"
    )
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💰 Статистика расходов"), KeyboardButton(text="🎯 Мои цели")],
            [KeyboardButton(text="✏️ Редактир��вать"), KeyboardButton(text="🗑️ Сброс")],
            [KeyboardButton(text="🎮 Игры"), KeyboardButton(text="💭 Цитата дня")],
            [KeyboardButton(text="🎯 Челлендж"), KeyboardButton(text="🏆 Мои достижения")],
            [KeyboardButton(text="ℹ️ Справка")]
        ],
        resize_keyboard=True
    )
    
    await message.answer("Выбери действие:", reply_markup=keyboard)

@router.message(Command("help"))
async def help_handler(message: types.Message):
    """Справка"""
    text = """
📖 СПРАВКА ПО ИСПОЛЬЗОВАНИЮ:

**Добавить расход:**
еда 5000
такси 15000
покупка одежда 100000

**Добавить доход:**
зарплата 500000
доход 50000
фриланс 20000

**Кнопки:**
💰 Статистика - просмотр расходов по категориям
🎯 Мои цели - управление целями на день
📊 Статистика целей - прогресс целей
✏️ Редактировать - изменить или удалить транзакцию
🗑️ Сброс - удалить все данные
🎮 Игры - сыграй в мини-игры
💭 Цитата дня - получи мотивацию
🎯 Челлендж - ежедневный вызов
🏆 Мои достижения - твои награды

**Примеры категорий расходов:**
🍔 еда, burger, pizza, кафе, ресторан
🚕 такси, метро, бензин, транспорт
🎬 netflix, spotify (подписки)
🛍️ магазин, одежда, шоппинг
"""
    await message.answer(text)

def register(dp):
    dp.include_router(router)
