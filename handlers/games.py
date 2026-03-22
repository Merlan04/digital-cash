# handlers/games.py (НОВЫЙ - Рулетка удачи)
from aiogram import types, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import random

router = Router()

class RouletteStates(StatesGroup):
    waiting_for_bet = State()

@router.message(lambda m: m.text == "🎮 Рулетка удачи")
async def roulette_menu(message: types.Message, state: FSMContext):
    """Меню рулетки"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Играть", callback_data="play_roulette")],
        [InlineKeyboardButton(text="📋 Правила", callback_data="roulette_rules")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_from_roulette")]
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
    
    await callback.message.answer(
        "🎲 Напиши число от 1 до 10:\n\n"
        "✅ Угадаешь - получишь +50,000 сўм!\n"
        "❌ Не угадаешь - просто сыграешь ещё раз 😊"
    )
    await callback.answer()

@router.message(RouletteStates.waiting_for_bet)
async def check_bet(message: types.Message, state: FSMContext):
    """Проверить ставку"""
    try:
        user_number = int(message.text)
        if user_number < 1 or user_number > 10:
            await message.answer("❌ Число должно быть от 1 до 10!")
            return
        
        data = await state.get_data()
        secret = data['secret_number']
        
        if user_number == secret:
            await message.answer(
                f"🎉 ПОБЕДА! 🎉\n\n"
                f"Ты угадал число {secret}!\n"
                f"Получил бонус: +50,000 сўм 💰"
            )
        else:
            await message.answer(
                f"❌ Не повезло! 😅\n\n"
                f"Ты выбрал: {user_number}\n"
                f"Правильный ответ: {secret}\n\n"
                f"Попробуй ещё раз! 🎲"
            )
        
        await state.clear()
    except ValueError:
        await message.answer("❌ Введи число!")

@router.callback_query(lambda c: c.data == "roulette_rules")
async def roulette_rules(callback: types.CallbackQuery):
    """Показать правила"""
    text = """
📋 ПРАВИЛА РУЛЕТКИ УДАЧИ:

1️⃣ Выбери число от 1 до 10
2️⃣ Если угадаешь - получишь +50,000 сўм
3️⃣ Если не угадаешь - просто сыграешь ещё
4️⃣ Можешь играть столько раз, сколько хочешь!

🎲 Шанс выигрыша: 10%
💰 Награда за победу: +50,000 сўм

Удачи! 🍀
"""
    await callback.message.answer(text)
    await callback.answer()

@router.callback_query(lambda c: c.data == "back_from_roulette")
async def back_from_roulette(callback: types.CallbackQuery, state: FSMContext):
    """Вернуться в меню"""
    await state.clear()
    await callback.message.answer("🔙 Вернулся в главное меню")
    await callback.answer()

def register(dp):
    dp.include_router(router)
