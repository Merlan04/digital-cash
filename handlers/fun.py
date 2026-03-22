# handlers/fun.py
from aiogram import types, Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import random

router = Router()

QUOTES = [
    "💭 Верь в себя - половина успеха! 💪",
    "💭 Каждый день - новая возможность! 🌟",
    "💭 Экономия деньги - инвестиция в будущее! 💰",
    "💭 Ты справишься! Не сдавайся! 🚀",
    "💭 Маленькие шаги - большие результаты! 📈",
    "💭 Финансовая свобода начинается с одного шага! 🎯"
]

DAILY_CHALLENGES = [
    "🎯 Челлендж: Не трати на кофе сегодня (сэкономь 15,000 сўм!)",
    "🎯 Челлендж: Приготовь обед дома вместо кафе (сэкономь 50,000 сўм!)",
    "🎯 Челлендж: Ходи пешком вместо такси (сэкономь 20,000 сўм!)",
    "🎯 Челлендж: Не покупай ничего лишнего сегодня! 🛑",
    "🎯 Челлендж: Запиши все расходы за день точно! 📝"
]

ACHIEVEMENTS = {
    "first_transaction": "🏅 Первая транзакция! Ты начал!",
    "100k": "💰 Ты отслеживаешь 100,000 сўм!",
    "1m": "💵 Молодец! 1,000,000 сўм под контролем!",
    "week_streak": "🔥 Неделя подряд без пропусков!",
    "smart_saver": "💎 Умный сбережник - 50% экономии!",
    "goal_master": "🎯 Мастер целей - 10 целей выполнено!",
    "game_lover": "🎮 Геймер - 20 игр сыграно!"
}

@router.message(lambda m: m.text == "💭 Цитата дня")
async def quote_handler(message: types.Message):
    """Случайная цитата"""
    quote = random.choice(QUOTES)
    await message.answer(quote)

@router.message(lambda m: m.text == "🎯 Челлендж")
async def challenge_handler(message: types.Message):
    """Ежедневный челлендж"""
    challenge = random.choice(DAILY_CHALLENGES)
    await message.answer(f"{challenge}\n\n✅ Сможешь выполнить?")

@router.message(lambda m: m.text == "🏆 Мои достижения")
async def achievements_handler(message: types.Message):
    """Показать достижения"""
    text = "🏆 ТВОИ ДОСТИЖЕНИЯ:\n\n"
    text += "🏅 Первая транзакция\n"
    text += "🔥 Неделя подряд\n"
    text += "💎 Умный сбережник\n\n"
    text += "_Продолжай так! Больше достижений ждут тебя!_"
    await message.answer(text)

def register(dp):
    dp.include_router(router)
