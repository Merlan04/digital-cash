from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.db import get_all, delete_transaction, update_transaction

router = Router()


class EditStates(StatesGroup):
    choosing_action = State()
    selecting_transaction = State()
    new_amount = State()
    confirm_delete = State()


@router.message(lambda m: m.text == "✏️ Редактировать")
async def edit_menu(message: types.Message, state: FSMContext):
    data = get_all(message.from_user.id)

    if not data:
        await message.answer("Нет транзакций для редактирования")
        return

    text = "📝 Ваши транзакции:\n\n"
    for i, (transaction_id, cat, amount, ttype, date) in enumerate(data, 1):
        icon = "💳" if ttype == "expense" else "💰"
        text += f"{i}. {icon} {cat} — {amount}so'm  ({date})\n"

    text += "\n🔢 Введите номер транзакции для редактирования (например: 1)"

    await message.answer(text)
    await state.set_state(EditStates.selecting_transaction)
    await state.update_data(transactions=data)


@router.message(EditStates.selecting_transaction)
async def select_transaction(message: types.Message, state: FSMContext):
    try:
        idx = int(message.text) - 1
        data = await state.get_data()
        transactions = data["transactions"]

        if idx < 0 or idx >= len(transactions):
            await message.answer("❌ Неверный номер")
            return

        transaction = transactions[idx]
        transaction_id = transaction[0]
        await state.update_data(selected_id=transaction_id, selected_transaction=transaction)

        transaction_id, cat, amount, ttype, date = transaction
        text = f"Выбранная транзакция:\n{cat} — {amount}so'm  ({date})\n\n"
        text += "Выберите действие:\n"
        text += "1️⃣ Изменить сумму\n"
        text += "2️⃣ Удалить"

        await message.answer(text)
        await state.set_state(EditStates.choosing_action)
    except ValueError:
        await message.answer("❌ Введите число")


@router.message(EditStates.choosing_action)
async def choose_action(message: types.Message, state: FSMContext):
    if message.text == "1️⃣" or message.text == "1":
        await message.answer("💰 Введите новую сумму:")
        await state.set_state(EditStates.new_amount)
    elif message.text == "2️⃣" or message.text == "2":
        await message.answer("⚠️ Точно удалить? Введите 'да' или 'нет'")
        await state.set_state(EditStates.confirm_delete)
    else:
        await message.answer("❌ Выберите 1 или 2")


@router.message(EditStates.new_amount)
async def set_new_amount(message: types.Message, state: FSMContext):
    try:
        new_amount = int(message.text)
        data = await state.get_data()
        transaction_id = data["selected_id"]

        update_transaction(transaction_id, new_amount)

        await message.answer(f"✅ Сумма изменена на {new_amount}so'm ")
        await state.clear()
    except ValueError:
        await message.answer("❌ Введите число")


@router.message(EditStates.confirm_delete)
async def confirm_delete(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        data = await state.get_data()
        transaction_id = data["selected_id"]

        delete_transaction(transaction_id)

        await message.answer("✅ Транзакция удалена")
        await state.clear()
    else:
        await message.answer("❌ Отменено")
        await state.clear()


def register(dp):
    dp.include_router(router)
