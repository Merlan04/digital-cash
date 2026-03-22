# handlers/goals.py (ОБНОВЛЁННЫЙ)
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.db import add_goal, get_today_goals, complete_goal, incomplete_goal, get_goal_stats
from datetime import datetime

router = Router()

class GoalStates(StatesGroup):
    waiting_for_goal = State()

@router.message(lambda m: m.text == "🎯 Мои цели")
async def show_goals(message: types.Message, state: FSMContext):
    """Показать цели на сегодня"""
    user_id = message.from_user.id
    goals = get_today_goals(user_id)
    
    if not goals:
        await message.answer(
            "📭 У вас еще нет целей на сегодня!\n\n"
            "Используйте /add_goal чтобы добавить новую цель"
        )
        return
    
    text = "🎯 <b>ВАШИ ЦЕЛИ НА СЕГОДНЯ</b>\n\n"
    
    for goal_id, goal_text, priority, status in goals:
        emoji_priority = "🔴" if priority == "high" else "🟡" if priority == "medium" else "🟢"
        emoji_status = "✅" if status == "completed" else "⏳"
        
        text += f"{emoji_status} {emoji_priority} {goal_text}\n"
    
    # Inline кнопки для отметки целей
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    for goal_id, goal_text, priority, status in goals:
        if status != "completed":
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(
                    text=f"✅ {goal_text[:20]}...",
                    callback_data=f"complete_goal_{goal_id}"
                )
            ])
    
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="➕ Добавить цель", callback_data="add_goal_btn")
    ])
    
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

@router.callback_query(lambda c: c.data.startswith("complete_goal_"))
async def complete_goal_callback(callback: types.CallbackQuery):
    """Отметить цель как выполненную"""
    goal_id = int(callback.data.split("_")[2])
    complete_goal(goal_id)
    
    await callback.answer("✅ Цель отмечена как выполненная!", show_alert=False)
    await callback.message.edit_text("✅ Цель выполнена! Отличная работа! 🎉")

@router.callback_query(lambda c: c.data == "add_goal_btn")
async def add_goal_btn(callback: types.CallbackQuery, state: FSMContext):
    """Начать добавление цели"""
    await callback.message.answer(
        "✍️ Напишите вашу цель:\n\n"
        "Примеры:\n"
        "• Пробежать 5 км\n"
        "• Прочитать 30 страниц книги\n"
        "• Завершить проект\n"
        "• Позвонить другу"
    )
    await state.set_state(GoalStates.waiting_for_goal)

@router.message(Command("add_goal"))
async def add_goal_command(message: types.Message, state: FSMContext):
    """Команда для добавления цели"""
    await message.answer(
        "✍️ Напишите вашу цель:\n\n"
        "Примеры:\n"
        "• Пробежать 5 км\n"
        "• Прочитать 30 страниц книги\n"
        "• Завершить проект\n"
        "• Позвонить другу"
    )
    await state.set_state(GoalStates.waiting_for_goal)

@router.message(GoalStates.waiting_for_goal)
async def process_goal_text(message: types.Message, state: FSMContext):
    """Обработать текст цели"""
    user_id = message.from_user.id
    goal_text = message.text
    
    # Добавляем цель с приоритетом medium по умолчанию
    add_goal(user_id, goal_text, priority='medium')
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎯 Мои цели")],
            [KeyboardButton(text="📊 Статистика целей")],
            [KeyboardButton(text="🔙 Назад в главное меню")],
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "✅ Цель добавлена! 🎉\n\n"
        "Теперь не забывайте отмечать выполненные цели!",
        reply_markup=keyboard
    )
    await state.clear()

@router.message(lambda m: m.text == "📊 Статистика целей")
async def goals_stats(message: types.Message):
    """Показать статистику целей"""
    user_id = message.from_user.id
    stats = get_goal_stats(user_id)
    
    text = "📊 <b>СТАТИСТИКА ЦЕЛЕЙ НА СЕГОДНЯ</b>\n\n"
    text += f"📋 Всего целей: {stats['total']}\n"
    text += f"✅ Выполнено: {stats['completed']}\n"
    text += f"⏳ В процессе: {stats['incomplete']}\n"
    text += f"📈 Процент выполнения: {stats['percentage']}%\n\n"
    
    if stats['incomplete_list']:
        text += "<b>❌ Невыполненные цели:</b>\n"
        for goal in stats['incomplete_list']:
            text += f"  • {goal}\n"
    else:
        text += "🎉 <b>Все цели выполнены! Отличная работа!</b>"
    
    await message.answer(text, parse_mode="HTML")

def register(dp):
    dp.include_router(router)
