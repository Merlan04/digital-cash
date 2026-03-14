from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.db import delete_all_transactions

router = Router()


class ResetStates(StatesGroup):
    confirm = State()


@router.message(lambda m: m.text == "🗑️ Сбросить данные")
async def reset_menu(message: types.Message, state: FSMContext):
    text = "⚠️ ВНИМАНИЕ! Это удалит ВСЕ ваши данные!\n\n"
    text += "Вы уверены? Введите 'да' или 'нет'"

    await message.answer(text)
    await state.set_state(ResetStates.confirm)


@router.message(ResetStates.confirm)
async def confirm_reset(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        delete_all_transactions(message.from_user.id)
        await message.answer("✅ Все данные удалены")
        await state.clear()
    else:
        await message.answer("❌ Отменено")
        await state.clear()


def register(dp):
    dp.include_router(router)