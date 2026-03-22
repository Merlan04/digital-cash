# handlers/games.py
from aiogram import types, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import random

router = Router()

class GameStates(StatesGroup):
    basketball_game = State()
    penalty_game = State()

@router.message(lambda m: m.text == "🎮 Игры")
async def games_menu(message: types.Message):
    """Меню игр"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏀 Бросок в кольцо", callback_data="basketball")],
        [InlineKeyboardButton(text="⚽ Пенальти", callback_data="penalty")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
    ])
    await message.answer("🎮 Выбери игру:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data == "basketball")
async def basketball_game(callback: types.CallbackQuery, state: FSMContext):
    """Игра бросок в кольцо"""
    secret_number = random.randint(1, 6)
    await state.update_data(secret_number=secret_number)
    await state.set_state(GameStates.basketball_game)
    
    await callback.message.answer(
        "🏀 Угадай число от 1 до 6!\n"
        "Если угадаешь - мяч в кольце! 🎯"
    )
    await callback.answer()

@router.message(GameStates.basketball_game)
async def basketball_answer(message: types.Message, state: FSMContext):
    """Проверка ответа"""
    try:
        user_number = int(message.text)
        data = await state.get_data()
        secret = data['secret_number']
        
        if user_number == secret:
            await message.answer("🎉 МЯच В КОЛЬЦЕ! Ты выиграл! 🏆")
        else:
            await message.answer(f"❌ Мимо! Мяч летит в другую сторону. Ответ был: {secret}")
        
        await state.clear()
    except ValueError:
        await message.answer("❌ Введи число от 1 до 6")

@router.callback_query(lambda c: c.data == "penalty")
async def penalty_game(callback: types.CallbackQuery, state: FSMContext):
    """Игра пенальти"""
    direction = random.choice(["left", "center", "right"])
    await state.update_data(penalty_direction=direction)
    await state.set_state(GameStates.penalty_game)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Влево", callback_data="penalty_left")],
        [InlineKeyboardButton(text="⬇️ В центр", callback_data="penalty_center")],
        [InlineKeyboardButton(text="➡️ Вправо", callback_data="penalty_right")]
    ])
    
    await callback.message.answer("⚽ Выбери сторону для удара!", reply_markup=keyboard)
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("penalty_"))
async def penalty_answer(callback: types.CallbackQuery, state: FSMContext):
    """Проверка ответа пенальти"""
    user_choice = callback.data.split("_")[1]
    data = await state.get_data()
    bot_direction = data['penalty_direction']
    
    choice_text = {"left": "⬅️ Влево", "center": "⬇️ В центр", "right": "➡️ Вправо"}
    
    if user_choice == bot_direction:
        await callback.message.answer(f"⚽ Ты выбрал: {choice_text[user_choice]}\n🥅 ГОЛЛЛ! ПОБЕДА! 🏆")
    else:
        await callback.message.answer(f"⚽ Ты выбрал: {choice_text[user_choice]}\n🥅 Вратарь поймал мяч! 😅")
    
    await state.clear()
    await callback.answer()

@router.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    """Вернуться в главное меню"""
    await callback.message.answer("🔙 Вернулся в главное меню")
    await callback.answer()

def register(dp):
    dp.include_router(router)
