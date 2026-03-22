# handlers/fun.py
from aiogram import types, Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
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

class RouletteStates(StatesGroup):
    waiting_for_bet = State()

@router.message(lambda m: m.text == "🎲 Рулетка удачи")
async def roulette_menu(message: types.Message, state: FSMContext):
    """Меню рулетки"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Играть", callback_data="play_roulette")],
        [InlineKeyboardButton(text="📋 Правила", callback_data="roulette_rules")]
    ])
    await message.answer(
        "🎲 РУЛЕТКА УДАЧИ\n\n"
        "Угадай число 1-10, выиграй бонус!\n"
        "Правильный ответ = +50,000 сўм 🎉",
        reply_markup=keyboard
    )

@router.callback_query(lambda c: c.data == "play_roulette")
async def play_roulette(callback: types.CallbackQuery, state: FSMContext):
    """Начать игру"""
    secret_number = random.randint(1, 10)
    await state.update_data(secret_number=secret_number)
    await state.set_state(RouletteStates.waiting_for_bet)
    
    await callback.message.answer("🎲 Напиши число от 1 до 10:")
    await callback.answer()

@router.message(RouletteStates.waiting_for_bet)
async def check_bet(message: types.Message, state: FSMContext):
    """Проверить ставку"""
    try:
        user_number = int(message.text)
        
        data = await state.get_data()
        secret = data['secret_number']
        
        if user_number < 1 or user_number > 10:
            await message.answer("❌ Число должно быть от 1 до 10!")
            return
        
        if user_number == secret:
            await message.answer(f"🎉 ПОБЕДА! Угадал число {secret}! +50,000 сўм 💰")
        else:
            await message.answer(f"❌ Не повезло! Число было {secret}")
        
        await state.clear()
    except ValueError:
        await message.answer("❌ Введи число от 1 до 10!")

@router.callback_query(lambda c: c.data == "roulette_rules")
async def roulette_rules(callback: types.CallbackQuery):
    """Правила"""
    await callback.message.answer("📋 Угадай число 1-10 и выиграй +50,000 сўм! 🎲")
    await callback.answer()

def register(dp):
    dp.include_router(router)
